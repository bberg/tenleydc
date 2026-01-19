"""
Scraper for Politics and Prose bookstore events
https://www.politics-prose.com/events
"""

from typing import List, Dict, Optional
from datetime import datetime
import re
import logging

from ..base_scraper import BaseScraper


class PoliticsProseScraper(BaseScraper):
    """Scraper for Politics and Prose bookstore events"""

    def __init__(self):
        super().__init__(
            source_id="politics-prose",
            source_name="Politics and Prose",
            base_url="https://www.politics-prose.com"
        )
        self.events_url = f"{self.base_url}/events"
        self.default_address = "5015 Connecticut Ave NW, Washington, DC 20008"

    def scrape(self) -> List[Dict]:
        """
        Scrape events from Politics and Prose.

        Returns:
            List of normalized event dictionaries
        """
        events = []

        try:
            self.logger.info(f"Scraping events from {self.events_url}")
            soup = self.fetch_page(self.events_url)

            # Find event listings
            # P&P uses various layouts, try multiple selectors
            event_containers = self._find_event_containers(soup)

            self.logger.info(f"Found {len(event_containers)} event containers")

            for container in event_containers:
                try:
                    raw_event = self._parse_event(container)
                    if raw_event:
                        normalized = self.normalize_event(raw_event)
                        events.append(normalized)
                except Exception as e:
                    self.logger.warning(f"Error parsing event: {e}")
                    continue

            self.logger.info(f"Successfully scraped {len(events)} events")

        except Exception as e:
            self.logger.error(f"Error scraping Politics and Prose: {e}")

        return events

    def _find_event_containers(self, soup) -> List:
        """Find event container elements on the page."""
        containers = []

        # Try different selectors based on P&P's site structure
        selectors = [
            'div.event-item',
            'article.event',
            'div.views-row',
            'div.event-listing',
            'li.event',
            'div[class*="event"]',
        ]

        for selector in selectors:
            found = soup.select(selector)
            if found:
                containers = found
                self.logger.debug(f"Found events using selector: {selector}")
                break

        # Fallback: look for common event patterns
        if not containers:
            # Look for links that contain "/event/" in the URL
            event_links = soup.find_all('a', href=re.compile(r'/event/'))
            seen_urls = set()
            for link in event_links:
                href = link.get('href', '')
                if href not in seen_urls:
                    seen_urls.add(href)
                    # Get the parent container
                    parent = link.find_parent(['div', 'article', 'li'])
                    if parent and parent not in containers:
                        containers.append(parent)

        return containers

    def _parse_event(self, container) -> Optional[Dict]:
        """Parse a single event from its container element."""
        event = {}

        # Extract title
        title_elem = container.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name'))
        if not title_elem:
            title_elem = container.find(['h2', 'h3', 'h4'])
        if not title_elem:
            title_elem = container.find('a')

        if title_elem:
            event['title'] = title_elem.get_text(strip=True)
            # Get link if available
            if title_elem.name == 'a':
                event['link'] = self._make_absolute_url(title_elem.get('href', ''))
            else:
                link_elem = title_elem.find('a') or container.find('a')
                if link_elem:
                    event['link'] = self._make_absolute_url(link_elem.get('href', ''))

        if not event.get('title'):
            return None

        # Extract date and time
        date_elem = container.find(class_=re.compile(r'date|time|when'))
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            parsed = self._parse_datetime(date_text)
            if parsed:
                event['date'] = parsed.get('date')
                event['time'] = parsed.get('time')

        # Look for datetime in meta tags or data attributes
        if not event.get('date'):
            time_elem = container.find('time')
            if time_elem:
                datetime_attr = time_elem.get('datetime')
                if datetime_attr:
                    try:
                        dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                        event['date'] = dt.strftime('%Y-%m-%d')
                        event['time'] = dt.strftime('%H:%M')
                    except ValueError:
                        pass

        # Extract description
        desc_elem = container.find(class_=re.compile(r'description|summary|content|body'))
        if not desc_elem:
            desc_elem = container.find('p')
        if desc_elem:
            event['description'] = desc_elem.get_text(strip=True)[:500]

        # Extract location (P&P has multiple locations)
        location_elem = container.find(class_=re.compile(r'location|venue|place'))
        if location_elem:
            location_text = location_elem.get_text(strip=True)
            event['location'] = self._normalize_location(location_text)
            event['address'] = self._get_address_for_location(location_text)
        else:
            event['location'] = self.source_name
            event['address'] = self.default_address

        # Extract image
        img_elem = container.find('img')
        if img_elem:
            img_src = img_elem.get('src') or img_elem.get('data-src')
            if img_src:
                event['image_url'] = self._make_absolute_url(img_src)

        # Check if free
        text_content = container.get_text().lower()
        event['free'] = 'free' in text_content

        # Check for registration
        event['registration_required'] = any(
            keyword in text_content
            for keyword in ['register', 'rsvp', 'sign up', 'ticket']
        )

        # Set category
        event['category'] = 'literary'

        # Generate ID from URL or title
        if event.get('link'):
            # Extract ID from URL like /event/12345
            match = re.search(r'/event/(\d+)', event['link'])
            if match:
                event['id'] = match.group(1)

        return event

    def _parse_datetime(self, text: str) -> Optional[Dict]:
        """Parse date and time from text."""
        result = {}

        # Common patterns for P&P events
        # "January 15, 2025 at 7:00 PM"
        # "Mon, Jan 15 | 7:00 PM"
        # "Tuesday, January 15, 2025 7:00pm"

        date_patterns = [
            r'(\w+)\s+(\d{1,2}),?\s+(\d{4})',  # January 15, 2025
            r'(\w+),?\s+(\w+)\s+(\d{1,2})',     # Mon, Jan 15
            r'(\d{1,2})/(\d{1,2})/(\d{2,4})',   # 01/15/2025
        ]

        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(am|pm)',     # 7:00 PM
            r'(\d{1,2})\s*(am|pm)',              # 7 PM
        ]

        # Try to extract date
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                try:
                    if len(groups) == 3 and groups[0].isalpha():
                        # Month Day, Year format
                        month_str = groups[0]
                        day = int(groups[1])
                        year = int(groups[2])

                        # Parse month
                        month_map = {
                            'january': 1, 'jan': 1,
                            'february': 2, 'feb': 2,
                            'march': 3, 'mar': 3,
                            'april': 4, 'apr': 4,
                            'may': 5,
                            'june': 6, 'jun': 6,
                            'july': 7, 'jul': 7,
                            'august': 8, 'aug': 8,
                            'september': 9, 'sep': 9, 'sept': 9,
                            'october': 10, 'oct': 10,
                            'november': 11, 'nov': 11,
                            'december': 12, 'dec': 12,
                        }
                        month = month_map.get(month_str.lower())
                        if month:
                            result['date'] = f"{year:04d}-{month:02d}-{day:02d}"
                            break
                except (ValueError, KeyError):
                    continue

        # Try to extract time
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                try:
                    hour = int(groups[0])
                    minute = int(groups[1]) if len(groups) > 2 else 0
                    ampm = groups[-1].lower()

                    if ampm == 'pm' and hour != 12:
                        hour += 12
                    elif ampm == 'am' and hour == 12:
                        hour = 0

                    result['time'] = f"{hour:02d}:{minute:02d}"
                    break
                except ValueError:
                    continue

        return result if result else None

    def _normalize_location(self, location_text: str) -> str:
        """Normalize P&P location names."""
        location_lower = location_text.lower()

        if 'connecticut' in location_lower or 'conn ave' in location_lower:
            return "Politics and Prose - Connecticut Ave"
        elif 'union market' in location_lower:
            return "Politics and Prose - Union Market"
        elif 'wharf' in location_lower:
            return "Politics and Prose - The Wharf"
        else:
            return self.source_name

    def _get_address_for_location(self, location_text: str) -> str:
        """Get address for P&P location."""
        location_lower = location_text.lower()

        addresses = {
            'connecticut': "5015 Connecticut Ave NW, Washington, DC 20008",
            'union market': "1270 5th St NE, Washington, DC 20002",
            'wharf': "70 District Square SW, Washington, DC 20024",
        }

        for key, address in addresses.items():
            if key in location_lower:
                return address

        return self.default_address

    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute."""
        if not url:
            return ''
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return f"{self.base_url}{url}"
        return f"{self.base_url}/{url}"
