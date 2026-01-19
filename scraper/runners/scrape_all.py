#!/usr/bin/env python3
"""
Main entry point for running all Tennally's Almanac scrapers
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scraper.scrapers import PoliticsProseScraper, DCLibraryScraper
from scraper.utils.deduplication import deduplicate_events, merge_duplicate_events
from scraper.config import DATA_DIR, CATEGORIES

# Try to import Playwright scrapers
try:
    from scraper.scrapers.politics_prose_pw import PoliticsProsePlaywrightScraper
    from scraper.scrapers.dc_library_pw import DCLibraryPlaywrightScraper
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


# Map scraper IDs to classes (regular scrapers)
SCRAPER_REGISTRY = {
    'politics_prose': PoliticsProseScraper,
    'dc_library': DCLibraryScraper,
}

# Playwright-based scrapers (used when --playwright flag is set or regular scrapers fail)
PLAYWRIGHT_REGISTRY = {
    'politics_prose': 'PoliticsProsePlaywrightScraper',
    'dc_library': 'DCLibraryPlaywrightScraper',
} if PLAYWRIGHT_AVAILABLE else {}


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging for the scraper."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger('scraper')


def load_sources() -> List[Dict]:
    """Load source configurations from JSON file."""
    sources_file = DATA_DIR / 'sources.json'

    if not sources_file.exists():
        logging.warning(f"Sources file not found: {sources_file}")
        return []

    with open(sources_file, 'r') as f:
        data = json.load(f)

    return data.get('event_sources', [])


def run_scraper(source: Dict, logger: logging.Logger, use_playwright: bool = False) -> List[Dict]:
    """
    Run a single scraper based on source configuration.

    Args:
        source: Source configuration dictionary
        logger: Logger instance
        use_playwright: Use Playwright-based scraper for JavaScript-rendered sites

    Returns:
        List of scraped events
    """
    scraper_id = source.get('scraper')

    # Determine which registry to use
    if use_playwright and scraper_id in PLAYWRIGHT_REGISTRY:
        logger.info(f"Using Playwright scraper for: {source.get('name', scraper_id)}")
        try:
            if scraper_id == 'politics_prose':
                scraper = PoliticsProsePlaywrightScraper()
            elif scraper_id == 'dc_library':
                scraper = DCLibraryPlaywrightScraper()
            else:
                logger.warning(f"No Playwright scraper for: {scraper_id}")
                return []

            events = scraper.run()
            logger.info(f"Scraped {len(events)} events from {source.get('name')}")
            return events

        except Exception as e:
            logger.error(f"Playwright scraper error for {scraper_id}: {e}")
            logger.info("Falling back to regular scraper...")

    # Use regular scraper
    if scraper_id not in SCRAPER_REGISTRY:
        logger.warning(f"Unknown scraper: {scraper_id}")
        return []

    logger.info(f"Running scraper: {source.get('name', scraper_id)}")

    try:
        scraper_class = SCRAPER_REGISTRY[scraper_id]
        scraper = scraper_class()
        events = scraper.scrape()

        logger.info(f"Scraped {len(events)} events from {source.get('name')}")
        return events

    except Exception as e:
        logger.error(f"Error running scraper {scraper_id}: {e}")
        # If regular scraper fails and Playwright is available, try Playwright
        if not use_playwright and PLAYWRIGHT_AVAILABLE and scraper_id in PLAYWRIGHT_REGISTRY:
            logger.info(f"Regular scraper failed, trying Playwright for {scraper_id}...")
            return run_scraper(source, logger, use_playwright=True)
        return []


def save_events(events: List[Dict], output_file: Path, logger: logging.Logger):
    """
    Save events to JSON file.

    Args:
        events: List of events to save
        output_file: Path to output file
        logger: Logger instance
    """
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Add metadata
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'event_count': len(events),
        'events': events
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    logger.info(f"Saved {len(events)} events to {output_file}")


def generate_markdown_events(events: List[Dict], output_dir: Path, logger: logging.Logger):
    """
    Generate markdown files for Hugo content.

    Args:
        events: List of events
        output_dir: Directory to write markdown files
        logger: Logger instance
    """
    events_dir = output_dir / 'events'
    events_dir.mkdir(parents=True, exist_ok=True)

    for event in events:
        event_id = event.get('id', '').replace('/', '-')
        if not event_id:
            continue

        # Create frontmatter
        frontmatter = {
            'title': event.get('title', ''),
            'date': event.get('date', ''),
            'time': event.get('time', ''),
            'end_time': event.get('end_time', ''),
            'location': event.get('location', ''),
            'address': event.get('address', ''),
            'category': event.get('category', 'community'),
            'free': event.get('free', True),
            'registration_required': event.get('registration_required', False),
            'link': event.get('link', ''),
            'source': event.get('source', ''),
            'tags': event.get('tags', []),
            'draft': False,
        }

        # Build markdown content
        content_lines = [
            '---',
        ]

        for key, value in frontmatter.items():
            if isinstance(value, list):
                content_lines.append(f'{key}:')
                for item in value:
                    content_lines.append(f'  - "{item}"')
            elif isinstance(value, bool):
                content_lines.append(f'{key}: {str(value).lower()}')
            elif isinstance(value, str) and value:
                # Escape quotes in strings
                escaped = value.replace('"', '\\"')
                content_lines.append(f'{key}: "{escaped}"')
            elif value:
                content_lines.append(f'{key}: {value}')

        content_lines.extend([
            '---',
            '',
            event.get('description', ''),
        ])

        # Write file
        filename = f"{event.get('date', 'undated')}-{event_id}.md"
        filepath = events_dir / filename

        with open(filepath, 'w') as f:
            f.write('\n'.join(content_lines))

    logger.info(f"Generated {len(events)} markdown files in {events_dir}")


def main():
    """Main entry point for the scraper."""
    parser = argparse.ArgumentParser(
        description="Scrape events for Tennally's Almanac"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '-s', '--source',
        help='Run only a specific source (by ID)'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=DATA_DIR / 'events.json',
        help='Output file for scraped events'
    )
    parser.add_argument(
        '--markdown',
        action='store_true',
        help='Also generate markdown files for Hugo'
    )
    parser.add_argument(
        '--markdown-dir',
        type=Path,
        default=PROJECT_ROOT / 'content',
        help='Directory for markdown output'
    )
    parser.add_argument(
        '--no-dedupe',
        action='store_true',
        help='Skip deduplication'
    )
    parser.add_argument(
        '--merge-dupes',
        action='store_true',
        help='Merge duplicate events instead of removing them'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run scrapers but do not save output'
    )
    parser.add_argument(
        '--playwright',
        action='store_true',
        help='Use Playwright-based scrapers for better JavaScript support'
    )

    args = parser.parse_args()
    logger = setup_logging(args.verbose)

    logger.info("Starting Tennally's Almanac scraper")

    # Load source configurations
    sources = load_sources()

    if not sources:
        logger.error("No sources configured")
        return 1

    # Filter to specific source if requested
    if args.source:
        sources = [s for s in sources if s.get('id') == args.source]
        if not sources:
            logger.error(f"Source not found: {args.source}")
            return 1

    # Run scrapers
    all_events = []

    for source in sources:
        events = run_scraper(source, logger, use_playwright=args.playwright)
        all_events.extend(events)

    logger.info(f"Total events scraped: {len(all_events)}")

    # Deduplication
    if not args.no_dedupe and len(all_events) > 0:
        if args.merge_dupes:
            all_events = merge_duplicate_events(all_events)
            logger.info(f"Events after merging duplicates: {len(all_events)}")
        else:
            all_events = deduplicate_events(all_events)
            logger.info(f"Events after deduplication: {len(all_events)}")

    # Sort events by date
    all_events.sort(key=lambda e: (e.get('date', ''), e.get('time', '')))

    # Save output
    if not args.dry_run:
        save_events(all_events, args.output, logger)

        if args.markdown:
            generate_markdown_events(all_events, args.markdown_dir, logger)
    else:
        logger.info("Dry run - not saving output")
        # Print summary
        for event in all_events[:10]:
            logger.info(f"  - {event.get('date')}: {event.get('title')}")
        if len(all_events) > 10:
            logger.info(f"  ... and {len(all_events) - 10} more events")

    logger.info("Scraping complete")
    return 0


if __name__ == '__main__':
    sys.exit(main())
