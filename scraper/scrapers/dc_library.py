"""
Scraper for DC Public Library events
Focused on Tenley-Friendship Branch
https://www.dclibrary.org/node/69141/events
"""

from typing import List, Dict, Optional
from datetime import datetime
import re
import logging

from ..base_scraper import BaseScraper


class DCLibraryScraper(BaseScraper):
    """Scraper for DC Public Library events at Tenley-Friendship Branch"""

    # Branch information
    BRANCHES = {
        'tenley-friendship': {
            'node_id': '69141',
            'name': 'Tenley-Friendship Library',
            'address': '4450 Wisconsin Ave NW, Washington, DC 20016'
        },
        'palisades': {
            'node_id': '69129',
            'name': 'Palisades Library',
            'address': '4901 V St NW, Washington, DC 20007'
        },
        'cleveland-park': {
            'node_id': '69101',
            'name': 'Cleveland Park Library',
            'address': '3310 Connecticut Ave NW, Washington, DC 20008'
        }
    }

    def __init__(self, branch: str = 'tenley-friendship'):
        branch_info = self.BRANCHES.get(branch, self.BRANCHES['tenley-friendship'])

        super().__init__(
            source_id=f"dc-library-{branch}",
            source_name=branch_info['name'],
            base_url="https://www.dclibrary.org"
        )

        self.branch = branch
        self.branch_info = branch_info
        self.events_url = f"{self.base_url}/node/{branch_info['node_id']}/events"

    def scrape(self) -> List[Dict]:
        """
        Scrape events from DC Library branch.

        Returns:
            List of normalized event dictionaries
        """
        events = []

        try:
            self.logger.info(f"Scraping events from {self.events_url}")
            soup = self.fetch_page(self.events_url)

            # Find event listings
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

            # Check for pagination and scrape additional pages
            events.extend(self._scrape_additional_pages(soup))

            self.logger.info(f"Successfully scraped {len(events)} events")

        except Exception as e:
            self.logger.error(f"Error scraping DC Library: {e}")

        return events

    def _find_event_containers(self, soup) -> List:
        """Find event container elements on the page."""
        containers = []

        # DCPL uses Drupal - try various selectors
        selectors = [
            'div.views-row',
            'article.event',
            'div.event-item',
            'div.node--type-event',
            'div.event-teaser',
            'li.event-listing',
            'div[class*="event"]',
        ]

        for selector in selectors:
            found = soup.select(selector)
            if found:
                containers = found
                self.logger.debug(f"Found events using selector: {selector}")
                break

        return containers

    def _parse_event(self, container) -> Optional[Dict]:
        """Parse a single event from its container element."""
        event = {}

        # Extract title
        title_elem = container.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name'))
        if not title_elem:
            title_elem = container.find(['h2', 'h3', 'h4'])
        if not title_elem:
            title_elem = container.find('a', href=re.compile(r'/event/'))

        if title_elem:
            event['title'] = title_elem.get_text(strip=True)
            # Get link if available
            if title_elem.name == 'a':
                event['link'] = self._make_absolute_url(title_elem.get('href', ''))
            else:
                link_elem = title_elem.find('a') or container.find('a', href=re.compile(r'/event/'))
                if link_elem:
                    event['link'] = self._make_absolute_url(link_elem.get('href', ''))

        if not event.get('title'):
            return None

        # Extract date and time
        date_elem = container.find(class_=re.compile(r'date|time|when|field--name-field-date'))
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            parsed = self._parse_datetime(date_text)
            if parsed:
                event['date'] = parsed.get('date')
                event['time'] = parsed.get('time')
                event['end_time'] = parsed.get('end_time')

        # Look for datetime in structured data
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
        desc_elem = container.find(class_=re.compile(r'description|summary|body|field--name-body'))
        if not desc_elem:
            desc_elem = container.find('p')
        if desc_elem:
            event['description'] = desc_elem.get_text(strip=True)[:500]

        # Extract location (should be the branch)
        event['location'] = self.branch_info['name']
        event['address'] = self.branch_info['address']

        # Check for different location in event
        location_elem = container.find(class_=re.compile(r'location|venue|branch'))
        if location_elem:
            location_text = location_elem.get_text(strip=True)
            if location_text and location_text != self.branch_info['name']:
                event['location'] = location_text

        # Extract image
        img_elem = container.find('img')
        if img_elem:
            img_src = img_elem.get('src') or img_elem.get('data-src')
            if img_src:
                event['image_url'] = self._make_absolute_url(img_src)

        # Extract category/tags
        event['category'] = self._determine_category(event)
        event['tags'] = self._extract_tags(container)

        # Library events are usually free
        event['free'] = True

        # Check for registration
        text_content = container.get_text().lower()
        event['registration_required'] = any(
            keyword in text_content
            for keyword in ['register', 'rsvp', 'sign up', 'limited space', 'reservation']
        )

        # Find registration link
        reg_link = container.find('a', href=re.compile(r'register|signup|rsvp', re.IGNORECASE))
        if reg_link:
            event['registration_url'] = self._make_absolute_url(reg_link.get('href', ''))

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

        # DCPL formats:
        # "Wednesday, January 15, 2025"
        # "Jan 15, 2025 10:30am - 11:30am"
        # "January 15 | 10:30 AM - 11:30 AM"

        # Date patterns
        date_patterns = [
            r'(\w+),?\s+(\w+)\s+(\d{1,2}),?\s+(\d{4})',  # Wednesday, January 15, 2025
            r'(\w+)\s+(\d{1,2}),?\s+(\d{4})',             # January 15, 2025
            r'(\w+)\s+(\d{1,2})\s*\|',                    # January 15 |
        ]

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

        # Try to extract date
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                try:
                    # Determine which group is the month
                    month = None
                    day = None
                    year = datetime.now().year  # Default to current year

                    for g in groups:
                        if g.lower() in month_map:
                            month = month_map[g.lower()]
                        elif g.isdigit():
                            num = int(g)
                            if num > 31:  # Likely a year
                                year = num
                            elif day is None:
                                day = num

                    if month and day:
                        result['date'] = f"{year:04d}-{month:02d}-{day:02d}"
                        break
                except (ValueError, KeyError):
                    continue

        # Time patterns - look for time range
        time_range_pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)?\s*[-–]\s*(\d{1,2}):?(\d{2})?\s*(am|pm)?'
        single_time_pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)'

        # Try time range first
        match = re.search(time_range_pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            start_hour = int(groups[0])
            start_min = int(groups[1]) if groups[1] else 0
            start_ampm = (groups[2] or groups[5] or 'am').lower()

            end_hour = int(groups[3])
            end_min = int(groups[4]) if groups[4] else 0
            end_ampm = (groups[5] or start_ampm).lower()

            # Convert to 24-hour
            if start_ampm == 'pm' and start_hour != 12:
                start_hour += 12
            elif start_ampm == 'am' and start_hour == 12:
                start_hour = 0

            if end_ampm == 'pm' and end_hour != 12:
                end_hour += 12
            elif end_ampm == 'am' and end_hour == 12:
                end_hour = 0

            result['time'] = f"{start_hour:02d}:{start_min:02d}"
            result['end_time'] = f"{end_hour:02d}:{end_min:02d}"
        else:
            # Try single time
            match = re.search(single_time_pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                hour = int(groups[0])
                minute = int(groups[1]) if groups[1] else 0
                ampm = groups[2].lower()

                if ampm == 'pm' and hour != 12:
                    hour += 12
                elif ampm == 'am' and hour == 12:
                    hour = 0

                result['time'] = f"{hour:02d}:{minute:02d}"

        return result if result else None

    def _determine_category(self, event: Dict) -> str:
        """Determine event category based on title and description."""
        text = (event.get('title', '') + ' ' + event.get('description', '')).lower()

        category_keywords = {
            'family': ['children', 'kids', 'family', 'storytime', 'story time', 'toddler',
                      'baby', 'teen', 'youth', 'puppet', 'craft'],
            'literary': ['book', 'author', 'reading', 'poetry', 'writing', 'library'],
            'education': ['workshop', 'class', 'learn', 'training', 'tutorial', 'computer',
                         'technology', 'digital', 'homework', 'tutoring'],
            'community': ['community', 'meeting', 'club', 'group', 'social'],
            'art': ['art', 'craft', 'creative', 'drawing', 'painting'],
            'music': ['music', 'concert', 'performance', 'sing'],
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category

        return 'community'

    def _extract_tags(self, container) -> List[str]:
        """Extract tags from event container."""
        tags = []

        # Look for tag elements
        tag_elems = container.find_all(class_=re.compile(r'tag|category|label'))
        for elem in tag_elems:
            tag_text = elem.get_text(strip=True)
            if tag_text:
                tags.append(tag_text.lower())

        # Look for audience indicators
        text = container.get_text().lower()
        audience_tags = {
            'children': ['children', 'kids', 'ages 3-5', 'ages 5-8'],
            'teens': ['teen', 'ages 12-18', 'young adult'],
            'adults': ['adult', '18+', '21+'],
            'seniors': ['senior', '55+', '60+'],
            'all-ages': ['all ages', 'family', 'everyone'],
        }

        for tag, keywords in audience_tags.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)

        return list(set(tags))

    def _scrape_additional_pages(self, soup) -> List[Dict]:
        """Scrape additional pages if pagination exists."""
        additional_events = []

        # Look for pagination
        pager = soup.find(class_=re.compile(r'pager|pagination'))
        if not pager:
            return additional_events

        # Find next page links (limit to 3 additional pages)
        next_links = pager.find_all('a', href=re.compile(r'page='))
        pages_scraped = 0

        for link in next_links:
            if pages_scraped >= 3:
                break

            href = link.get('href', '')
            if href:
                try:
                    page_url = self._make_absolute_url(href)
                    self.logger.debug(f"Scraping additional page: {page_url}")
                    page_soup = self.fetch_page(page_url)

                    containers = self._find_event_containers(page_soup)
                    for container in containers:
                        try:
                            raw_event = self._parse_event(container)
                            if raw_event:
                                normalized = self.normalize_event(raw_event)
                                additional_events.append(normalized)
                        except Exception as e:
                            self.logger.warning(f"Error parsing event on page: {e}")

                    pages_scraped += 1

                except Exception as e:
                    self.logger.warning(f"Error fetching page {href}: {e}")

        return additional_events

    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute."""
        if not url:
            return ''
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return f"{self.base_url}{url}"
        return f"{self.base_url}/{url}"
