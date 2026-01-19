"""
Abstract base class for event scrapers
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import logging
import time

from .config import USER_AGENT, DEFAULT_TIMEOUT, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_DELAY


class BaseScraper(ABC):
    """Abstract base class for event scrapers"""

    def __init__(self, source_id: str, source_name: str, base_url: str):
        self.source_id = source_id
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })
        self.logger = logging.getLogger(f"scraper.{source_id}")

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape events from the source.

        Returns:
            List of normalized event dictionaries
        """
        pass

    def fetch_page(self, url: str, retry_count: int = DEFAULT_RETRY_COUNT) -> BeautifulSoup:
        """
        Fetch and parse a page with retry logic.

        Args:
            url: URL to fetch
            retry_count: Number of retries on failure

        Returns:
            BeautifulSoup object of parsed HTML
        """
        last_error = None

        for attempt in range(retry_count):
            try:
                self.logger.debug(f"Fetching {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=DEFAULT_TIMEOUT)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'lxml')
            except requests.RequestException as e:
                last_error = e
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(DEFAULT_RETRY_DELAY)

        raise last_error

    def normalize_event(self, raw_event: Dict) -> Dict:
        """
        Normalize event data to standard format.

        Args:
            raw_event: Raw event data from scraper

        Returns:
            Normalized event dictionary
        """
        # Generate a unique ID
        event_id = raw_event.get('id', '')
        if not event_id:
            # Create ID from title and date if not provided
            title_slug = self._slugify(raw_event.get('title', 'unknown'))
            date_str = raw_event.get('date', datetime.now().strftime('%Y%m%d'))
            event_id = f"{title_slug}-{date_str}"

        return {
            'id': f"{self.source_id}-{event_id}",
            'title': self._clean_text(raw_event.get('title', '')),
            'date': raw_event.get('date', ''),
            'end_date': raw_event.get('end_date', ''),
            'time': raw_event.get('time', ''),
            'end_time': raw_event.get('end_time', ''),
            'location': raw_event.get('location', self.source_name),
            'address': raw_event.get('address', ''),
            'category': raw_event.get('category', 'community'),
            'description': self._clean_text(raw_event.get('description', '')),
            'link': raw_event.get('link', ''),
            'image_url': raw_event.get('image_url', ''),
            'free': raw_event.get('free', True),
            'registration_required': raw_event.get('registration_required', False),
            'registration_url': raw_event.get('registration_url', ''),
            'tags': raw_event.get('tags', []),
            'source': self.source_id,
            'source_name': self.source_name,
            'scraped_at': datetime.now().isoformat()
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ''
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        return text[:50]  # Limit length

    def _parse_date(self, date_str: str, formats: List[str] = None) -> Optional[str]:
        """
        Parse date string to standard format.

        Args:
            date_str: Date string to parse
            formats: List of formats to try

        Returns:
            Date in YYYY-MM-DD format or None
        """
        if not date_str:
            return None

        if formats is None:
            formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%B %d, %Y',
                '%b %d, %Y',
                '%d %B %Y',
                '%d %b %Y',
            ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        self.logger.warning(f"Could not parse date: {date_str}")
        return None

    def _parse_time(self, time_str: str) -> Optional[str]:
        """
        Parse time string to standard format.

        Args:
            time_str: Time string to parse

        Returns:
            Time in HH:MM format or None
        """
        if not time_str:
            return None

        import re

        # Try common formats
        formats = [
            '%H:%M',
            '%I:%M %p',
            '%I:%M%p',
            '%I %p',
            '%I%p',
        ]

        # Clean the time string
        time_str = time_str.strip().upper()
        time_str = re.sub(r'\s+', ' ', time_str)

        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.strftime('%H:%M')
            except ValueError:
                continue

        self.logger.warning(f"Could not parse time: {time_str}")
        return None
