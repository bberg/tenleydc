"""
Playwright-based scraper for Politics and Prose events.
Uses browser automation to handle the JavaScript-rendered event list.
"""

import re
from datetime import datetime
from typing import List, Dict, Any
import hashlib

from bs4 import BeautifulSoup

from ..playwright_base import PlaywrightBaseScraper


class PoliticsProsePlaywrightScraper(PlaywrightBaseScraper):
    """
    Scraper for Politics and Prose bookstore events using Playwright.
    """

    def __init__(self):
        super().__init__(
            source_id='politics-prose',
            source_name='Politics and Prose',
            base_url='https://www.politics-prose.com/events'
        )
        self.address = '5015 Connecticut Ave NW'
        self.default_category = 'literary'

    async def scrape(self) -> List[Dict[str, Any]]:
        """Scrape events from Politics and Prose website."""
        events = []

        try:
            # Get the main events page - wait for event-list articles to load
            html = await self._get_page_content(
                self.base_url,
                wait_for_selector='article.event-list',
                wait_time=5000
            )

            soup = BeautifulSoup(html, 'lxml')

            # Events are in article.event-list elements
            event_elements = soup.select('article.event-list')
            print(f"Found {len(event_elements)} event elements")

            for element in event_elements:
                try:
                    event = self._parse_event_element(element)
                    if event and event.get('title') and event.get('date'):
                        events.append(self._normalize_event(event))
                except Exception as e:
                    print(f"Error parsing event: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping Politics and Prose: {e}")

        return events

    def _parse_event_element(self, element) -> Dict[str, Any]:
        """Parse a single event element."""
        event = {}

        # Extract title from .event-list__title or h3
        title_elem = (
            element.select_one('.event-list__title') or
            element.select_one('h3')
        )
        if title_elem:
            event['title'] = title_elem.get_text(strip=True)

        # Extract link from h3 a
        link_elem = element.select_one('h3 a') or element.select_one('.event-list__title a')
        if link_elem and link_elem.get('href'):
            href = link_elem['href']
            if not href.startswith('http'):
                href = f"https://www.politics-prose.com{href}"
            event['link'] = href

        # Extract date from .event-list__date--month and .event-list__date--day
        month_elem = element.select_one('.event-list__date--month')
        day_elem = element.select_one('.event-list__date--day')
        if month_elem and day_elem:
            month = month_elem.get_text(strip=True)
            day = day_elem.get_text(strip=True)
            event['date'] = self._parse_date(f"{month} {day}")

        # Extract category from .event-list__tags or .event-tag__term
        tag_elem = (
            element.select_one('.event-tag__term') or
            element.select_one('.event-list__tags a')
        )
        if tag_elem:
            category = tag_elem.get_text(strip=True).lower()
            event['category'] = self._map_category(category)
        else:
            event['category'] = self.default_category

        # Extract description from .event-list__body
        desc_elem = element.select_one('.event-list__body')
        if desc_elem:
            event['description'] = desc_elem.get_text(strip=True)[:500]

        # Extract time and date details from .event-list__details--item
        detail_items = element.select('.event-list__details--item')
        for item in detail_items:
            label_elem = item.select_one('.event-list__details--label')
            if label_elem:
                label = label_elem.get_text(strip=True).lower()
                # Get the full text and remove the label
                full_text = item.get_text(strip=True)
                value = full_text.replace(label_elem.get_text(strip=True), '').strip()

                if 'date' in label:
                    # Parse full date like "Fri, 1/2/2026"
                    event['full_date'] = value
                    parsed = self._parse_full_date(value)
                    if parsed:
                        event['date'] = parsed
                elif 'time' in label:
                    event['time'] = value
                elif 'place' in label:
                    # Clean up place text
                    event['location_detail'] = ' '.join(value.split())

        # Set defaults
        event['location'] = self.source_name
        event['address'] = self.address
        event['free'] = True  # Most P&P events are free

        # Generate ID
        if event.get('title') and event.get('date'):
            id_string = f"pp-{event['title']}-{event['date']}"
            event['id'] = hashlib.md5(id_string.encode()).hexdigest()[:12]

        return event

    def _parse_date(self, date_text: str) -> str:
        """Parse short date like 'Jan 02' into YYYY-MM-DD format."""
        date_text = ' '.join(date_text.split())
        current_year = datetime.now().year

        # Try parsing "Jan 02" format
        try:
            # Add year
            date_with_year = f"{date_text} {current_year}"
            parsed = datetime.strptime(date_with_year, '%b %d %Y')

            # If the date is in the past, assume next year
            if parsed < datetime.now():
                parsed = parsed.replace(year=current_year + 1)

            return parsed.strftime('%Y-%m-%d')
        except ValueError:
            pass

        return date_text

    def _parse_full_date(self, date_text: str) -> str:
        """Parse full date like 'Fri, 1/2/2026' into YYYY-MM-DD format."""
        date_text = ' '.join(date_text.split())

        patterns = [
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),  # 1/2/2026
            (r'(\w+),?\s*(\d{1,2})/(\d{1,2})/(\d{4})', None),  # Fri, 1/2/2026
        ]

        # Try to extract just the date part
        match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_text)
        if match:
            try:
                parsed = datetime.strptime(match.group(), '%m/%d/%Y')
                return parsed.strftime('%Y-%m-%d')
            except ValueError:
                pass

        return None

    def _map_category(self, category: str) -> str:
        """Map P&P category to our category system."""
        category = category.lower()

        if 'fiction' in category:
            return 'literary'
        elif 'children' in category or 'kids' in category:
            return 'family'
        elif 'poetry' in category:
            return 'literary'
        elif 'history' in category or 'politics' in category:
            return 'literary'
        elif 'music' in category:
            return 'music'

        return self.default_category


def scrape() -> List[Dict[str, Any]]:
    """Entry point for the scraper runner."""
    scraper = PoliticsProsePlaywrightScraper()
    return scraper.run()


if __name__ == '__main__':
    events = scrape()
    print(f"Found {len(events)} events")
    for event in events[:10]:
        print(f"  - {event.get('date')}: {event.get('title')}")
