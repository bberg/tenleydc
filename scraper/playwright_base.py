"""
Base class for Playwright-based scrapers that can handle sites with anti-bot protection.
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PlaywrightBaseScraper(ABC):
    """
    Base class for scrapers that use Playwright to render JavaScript
    and bypass anti-bot measures.
    """

    def __init__(self, source_id: str, source_name: str, base_url: str):
        self.source_id = source_id
        self.source_name = source_name
        self.base_url = base_url
        self.browser: Optional[Browser] = None

        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is not installed. Run: pip install playwright && playwright install chromium"
            )

    async def _init_browser(self, headless: bool = True):
        """Initialize the Playwright browser."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=headless)
        return self.browser

    async def _close_browser(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()

    async def _get_page_content(self, url: str, wait_for_selector: Optional[str] = None,
                                 wait_time: int = 2000) -> str:
        """
        Navigate to URL and return page HTML after JavaScript execution.

        Args:
            url: URL to fetch
            wait_for_selector: CSS selector to wait for before returning
            wait_time: Time to wait in milliseconds for dynamic content

        Returns:
            HTML content of the page
        """
        if not self.browser:
            await self._init_browser()

        page = await self.browser.new_page()

        try:
            # Set a realistic user agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            await page.goto(url, wait_until='networkidle')

            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector, timeout=10000)
            else:
                await page.wait_for_timeout(wait_time)

            content = await page.content()
            return content

        finally:
            await page.close()

    @abstractmethod
    async def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape events from the source.
        Must be implemented by subclasses.

        Returns:
            List of event dictionaries
        """
        pass

    def run(self) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper to run the async scraper.
        """
        return asyncio.run(self._run_scraper())

    async def _run_scraper(self) -> List[Dict[str, Any]]:
        """Run the scraper with proper browser lifecycle management."""
        try:
            await self._init_browser()
            events = await self.scrape()
            return events
        finally:
            await self._close_browser()

    def _normalize_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize event data to a standard format.
        """
        normalized = {
            'id': event.get('id', ''),
            'title': event.get('title', '').strip(),
            'date': event.get('date'),
            'time': event.get('time', ''),
            'location': event.get('location', self.source_name),
            'address': event.get('address', ''),
            'category': event.get('category', ''),
            'description': event.get('description', '').strip(),
            'link': event.get('link', ''),
            'free': event.get('free', False),
            'source': self.source_id,
            'scraped_at': datetime.now().isoformat()
        }
        return normalized
