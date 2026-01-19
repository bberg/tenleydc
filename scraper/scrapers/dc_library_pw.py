"""
Playwright-based scraper for DC Public Library events.
Uses browser automation to handle the dynamic event calendar.
"""

import re
from datetime import datetime
from typing import List, Dict, Any
import hashlib

from bs4 import BeautifulSoup

from ..playwright_base import PlaywrightBaseScraper


class DCLibraryPlaywrightScraper(PlaywrightBaseScraper):
    """
    Scraper for DC Public Library events using Playwright.
    Focuses on Tenley-Friendship Library branch events.
    """

    def __init__(self, branch: str = 'Tenley-Friendship'):
        super().__init__(
            source_id='dc-library-tenley',
            source_name=f'{branch} Library',
            base_url='https://dclibrary.libnet.info/events'
        )
        self.branch = branch
        self.address = '4450 Wisconsin Ave NW'
        self.default_category = 'family'

        # URL with location filter
        self.events_url = f'https://dclibrary.libnet.info/events?l={branch.replace(" ", "+")}+Neighborhood+Library'

    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrape events from DC Library website."""
        events = []

        try:
            # Get the events page for this branch
            # DC Library uses Communico system with these selectors
            html = await self._get_page_content(
                self.events_url,
                wait_for_selector='.events-grid-cell-event, .eelisttitle, .amev-event-list',
                wait_time=5000
            )

            soup = BeautifulSoup(html, 'lxml')

            # DC Library Communico selectors (discovered via browser inspection)
            # Try grid view first, then list view
            event_elements = (
                soup.select('.events-grid-cell-event') or  # Grid view events
                soup.select('.amev-event-list > div') or   # Widget list events
                soup.select('[class*="eelisttitle"]')      # Event list items
            )

            # If we found eelisttitle, need to get parent containers
            if not event_elements:
                list_items = soup.select('.eelisttitle')
                event_elements = [item.find_parent('div') for item in list_items if item.find_parent('div')]

            for element in event_elements[:30]:  # Limit to 30 events
                try:
                    event = self._parse_event_element(element)
                    if event and event.get('title'):
                        events.append(self._normalize_event(event))
                except Exception as e:
                    print(f"Error parsing event: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping DC Library: {e}")

        return events

    def _parse_event_element(self, element) -> Dict[str, Any]:
        """Parse a single event element from DC Library Communico system."""
        event = {}

        # Extract title - DC Library Communico selectors
        title_elem = (
            element.select_one('.eelisttitle a') or          # List view title
            element.select_one('.amev-event-title a') or     # Widget title
            element.select_one('.events-grid-cell-event a') or  # Grid view
            element.select_one('a[href*="event"]')
        )
        if title_elem:
            event['title'] = title_elem.get_text(strip=True)

        # Extract date/time - Communico uses combined date/time fields
        date_elem = (
            element.select_one('.eelisttime.headingtext') or  # List view date/time
            element.select_one('.amev-event-time.headingtext') or  # Widget time
            element.select_one('.events-grid-cell-date') or   # Grid date
            element.select_one('.events-date-string.headingtext')
        )
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            # Parse combined date/time like "Tuesday, January 21, 2026 10:30 AM - 11:30 AM"
            parsed = self._parse_datetime(date_text)
            if parsed.get('date'):
                event['date'] = parsed['date']
            if parsed.get('time'):
                event['time'] = parsed['time']

        # Extract link
        link_elem = element.select_one('a[href*="event"]') or element.select_one('.eelisttitle a')
        if link_elem and link_elem.get('href'):
            href = link_elem['href']
            if not href.startswith('http'):
                href = f"https://dclibrary.libnet.info{href}"
            event['link'] = href

        # Extract description - Communico selectors
        desc_elem = (
            element.select_one('.eelistdesc') or             # List view description
            element.select_one('.amev-event-description') or  # Widget description
            element.select_one('.custom1') or                 # Subtitle/short desc
            element.select_one('p')
        )
        if desc_elem:
            event['description'] = desc_elem.get_text(strip=True)[:500]

        # Extract location/branch
        loc_elem = element.select_one('.eelocation, .venue, .branch')
        if loc_elem:
            event['location'] = loc_elem.get_text(strip=True)
        else:
            event['location'] = self.source_name

        # Determine category based on title/description
        event['category'] = self._determine_category(event)

        # Set defaults
        event['address'] = self.address
        event['free'] = True  # Library events are free

        # Generate ID
        if event.get('title') and event.get('date'):
            id_string = f"dcl-{event['title']}-{event['date']}"
            event['id'] = hashlib.md5(id_string.encode()).hexdigest()[:12]

        return event

    def _parse_datetime(self, text: str) -> Dict[str, str]:
        """Parse combined date/time text like 'Tuesday, January 21, 2026 10:30 AM - 11:30 AM'."""
        result = {}
        text = ' '.join(text.split())

        # Try to extract date: "January 21, 2026" or "1/21/2026"
        date_patterns = [
            (r'(\w+)\s+(\d{1,2}),?\s*(\d{4})', '%B %d %Y'),  # January 21, 2026
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),    # 1/21/2026
        ]

        for pattern, date_format in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = match.group()
                    parsed = datetime.strptime(date_str, date_format)
                    result['date'] = parsed.strftime('%Y-%m-%d')
                    break
                except ValueError:
                    continue

        # Try to extract time: "10:30 AM" or "10:30 AM - 11:30 AM"
        time_match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM))', text, re.IGNORECASE)
        if time_match:
            result['time'] = time_match.group(1)
            # Check for end time
            end_time_match = re.search(r'-\s*(\d{1,2}:\d{2}\s*(?:AM|PM))', text, re.IGNORECASE)
            if end_time_match:
                result['time'] = f"{time_match.group(1)} - {end_time_match.group(1)}"

        return result

    def _parse_date(self, date_text: str) -> str:
        """Parse date text into YYYY-MM-DD format."""
        date_text = ' '.join(date_text.split())

        patterns = [
            (r'(\w+)\s+(\d{1,2}),?\s*(\d{4})', '%B %d %Y'),
            (r'(\d{1,2})/(\d{1,2})/(\d{2,4})', '%m/%d/%Y'),
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
            (r'(\w+)\s+(\d{1,2})', '%B %d'),  # January 15 (assume current year)
        ]

        for pattern, date_format in patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    date_str = match.group()
                    if '%Y' not in date_format:
                        date_str += f' {datetime.now().year}'
                        date_format += ' %Y'
                    parsed = datetime.strptime(date_str, date_format)
                    return parsed.strftime('%Y-%m-%d')
                except ValueError:
                    continue

        return date_text

    def _determine_category(self, event: Dict[str, Any]) -> str:
        """Determine event category based on title and description."""
        text = f"{event.get('title', '')} {event.get('description', '')}".lower()

        if any(word in text for word in ['storytime', 'children', 'kids', 'baby', 'toddler']):
            return 'family'
        elif any(word in text for word in ['teen', 'youth']):
            return 'family'
        elif any(word in text for word in ['book club', 'reading', 'author']):
            return 'literary'
        elif any(word in text for word in ['yoga', 'fitness', 'wellness', 'health']):
            return 'family'
        elif any(word in text for word in ['movie', 'film', 'screening']):
            return 'entertainment'
        elif any(word in text for word in ['class', 'workshop', 'learn', 'esl', 'english']):
            return 'education'
        elif any(word in text for word in ['craft', 'art', 'music']):
            return 'entertainment'

        return self.default_category


def scrape(branch: str = 'Tenley-Friendship') -> List[Dict[str, Any]]:
    """Entry point for the scraper runner."""
    scraper = DCLibraryPlaywrightScraper(branch=branch)
    return scraper.run()


if __name__ == '__main__':
    events = scrape()
    print(f"Found {len(events)} events")
    for event in events[:5]:
        print(f"  - {event.get('title')} ({event.get('date')})")
