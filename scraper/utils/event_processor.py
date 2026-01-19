"""
Event processing utilities for Tennally's Almanac.
Processes raw scraped data and merges with existing events.
"""

import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


def parse_pp_date(date_raw: str) -> Optional[str]:
    """
    Parse Politics & Prose date format like 'Fri, 1/2/2026' to YYYY-MM-DD.
    """
    if not date_raw:
        return None

    # Try to extract date pattern like "1/2/2026"
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_raw)
    if match:
        month, day, year = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    return None


def process_pp_events(raw_events: List[Dict]) -> List[Dict[str, Any]]:
    """
    Process raw Politics & Prose events into normalized format.

    Args:
        raw_events: List of raw event dicts from Chrome extraction

    Returns:
        List of normalized event dicts
    """
    processed = []

    for raw in raw_events:
        if not raw.get('title'):
            continue

        event = {
            'source': 'politics-prose',
            'location': 'Politics and Prose',
            'address': '5015 Connecticut Ave NW',
            'free': True,
            'category': 'literary',
        }

        # Title - clean up
        title = raw.get('title', '').strip()
        # Remove "— AT CONN AVE" or "— AT THE WHARF" suffixes
        title = re.sub(r'\s*[—-]\s*(AT\s+)?(CONN\s+AVE|THE\s+WHARF).*$', '', title, flags=re.IGNORECASE)
        event['title'] = title

        # Date
        date = parse_pp_date(raw.get('dateRaw', ''))
        if not date:
            continue  # Skip events without valid dates
        event['date'] = date

        # Time
        if raw.get('time'):
            event['time'] = raw['time']

        # Link
        if raw.get('link'):
            event['link'] = raw['link']

        # Description
        if raw.get('description'):
            desc = raw['description'].strip()
            # Remove trailing "..." if present
            desc = re.sub(r'\.\.\.$', '', desc).strip()
            event['description'] = desc[:500]

        # Location - check if at The Wharf
        place = raw.get('place', '').lower()
        if 'wharf' in place:
            event['location'] = 'Politics and Prose at The Wharf'
            event['address'] = '70 District Square SW'

        # Category based on raw category
        raw_cat = raw.get('category', '').lower()
        if 'child' in raw_cat or 'teen' in raw_cat:
            event['category'] = 'family'
        elif 'fiction' in raw_cat or 'non fiction' in raw_cat:
            event['category'] = 'literary'

        # Generate ID
        id_str = f"pp-{date}-{title[:30]}".lower()
        id_str = re.sub(r'[^a-z0-9-]', '', id_str)
        event['id'] = id_str[:40]

        processed.append(event)

    return processed


def merge_events(existing: List[Dict], new_events: List[Dict],
                 prefer_new: bool = False) -> List[Dict]:
    """
    Merge new events with existing events, avoiding duplicates.

    Args:
        existing: List of existing events
        new_events: List of new events to merge
        prefer_new: If True, prefer new event data for duplicates

    Returns:
        Merged list of events
    """
    # Index existing events by date+title hash
    existing_index = {}
    for event in existing:
        key = _event_key(event)
        existing_index[key] = event

    # Add new events, checking for duplicates
    added = 0
    updated = 0

    for event in new_events:
        key = _event_key(event)

        if key in existing_index:
            if prefer_new:
                # Update existing with new data
                existing_index[key].update(event)
                updated += 1
        else:
            existing_index[key] = event
            added += 1

    print(f"Added {added} new events, updated {updated} existing events")

    # Return sorted by date
    merged = list(existing_index.values())
    merged.sort(key=lambda e: (e.get('date', ''), e.get('time', '')))

    return merged


def _event_key(event: Dict) -> str:
    """Generate a unique key for an event based on date and normalized title."""
    date = event.get('date', '')
    title = event.get('title', '').lower()
    # Normalize title - remove punctuation and extra spaces
    title = re.sub(r'[^\w\s]', '', title)
    title = ' '.join(title.split())[:50]

    key_str = f"{date}|{title}"
    return hashlib.md5(key_str.encode()).hexdigest()


def load_events(file_path: Path) -> List[Dict]:
    """Load events from JSON file."""
    if not file_path.exists():
        return []

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Handle both formats: {"events": [...]} and [...]
    if isinstance(data, dict):
        return data.get('events', [])
    return data


def save_events(events: List[Dict], file_path: Path):
    """Save events to JSON file."""
    output = {
        'events': events
    }

    with open(file_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Saved {len(events)} events to {file_path}")


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python event_processor.py <raw_events.json>")
        sys.exit(1)

    raw_file = Path(sys.argv[1])
    if not raw_file.exists():
        print(f"File not found: {raw_file}")
        sys.exit(1)

    # Load raw events
    with open(raw_file, 'r') as f:
        raw_events = json.load(f)

    # Process P&P events
    processed = process_pp_events(raw_events)
    print(f"Processed {len(processed)} events")

    # Load existing events
    data_dir = Path(__file__).parent.parent.parent / 'data'
    existing_events = load_events(data_dir / 'events.json')

    # Merge
    merged = merge_events(existing_events, processed)

    # Save
    save_events(merged, data_dir / 'events.json')
