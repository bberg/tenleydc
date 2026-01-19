"""
Event deduplication utilities for Tennally's Almanac
"""

from typing import List, Dict, Set, Tuple
from datetime import datetime
import re
import hashlib
from difflib import SequenceMatcher


def generate_event_hash(event: Dict) -> str:
    """
    Generate a hash for an event based on key fields.

    Args:
        event: Normalized event dictionary

    Returns:
        MD5 hash string
    """
    # Create a normalized string from key fields
    key_parts = [
        normalize_title(event.get('title', '') or ''),
        event.get('date', '') or '',
        event.get('time', '') or '',
        normalize_location(event.get('location', '') or '')
    ]
    key_string = '|'.join(key_parts).lower()
    return hashlib.md5(key_string.encode()).hexdigest()


def normalize_title(title: str) -> str:
    """
    Normalize event title for comparison.

    Args:
        title: Original title

    Returns:
        Normalized title
    """
    if not title:
        return ''

    # Convert to lowercase
    title = title.lower()

    # Remove common prefixes/suffixes
    prefixes = ['the ', 'a ', 'an ']
    for prefix in prefixes:
        if title.startswith(prefix):
            title = title[len(prefix):]

    # Remove punctuation and extra whitespace
    title = re.sub(r'[^\w\s]', '', title)
    title = ' '.join(title.split())

    return title.strip()


def normalize_location(location: str) -> str:
    """
    Normalize location name for comparison.

    Args:
        location: Original location

    Returns:
        Normalized location
    """
    if not location:
        return ''

    # Convert to lowercase
    location = location.lower()

    # Common location normalizations
    replacements = {
        'politics & prose': 'politics and prose',
        'p&p': 'politics and prose',
        'tenley-friendship library': 'tenley friendship library',
        'tenley friendship branch': 'tenley friendship library',
        'dc public library': 'dcpl',
    }

    for old, new in replacements.items():
        location = location.replace(old, new)

    # Remove punctuation and extra whitespace
    location = re.sub(r'[^\w\s]', '', location)
    location = ' '.join(location.split())

    return location.strip()


def title_similarity(title1: str, title2: str) -> float:
    """
    Calculate similarity ratio between two titles.

    Args:
        title1: First title
        title2: Second title

    Returns:
        Similarity ratio (0.0 to 1.0)
    """
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)
    return SequenceMatcher(None, norm1, norm2).ratio()


def is_duplicate(event1: Dict, event2: Dict,
                 title_threshold: float = 0.85,
                 check_time: bool = True) -> bool:
    """
    Check if two events are likely duplicates.

    Args:
        event1: First event
        event2: Second event
        title_threshold: Minimum title similarity to consider duplicate
        check_time: Whether to require matching times

    Returns:
        True if events are likely duplicates
    """
    # Must be on the same date
    if event1.get('date') != event2.get('date'):
        return False

    # Check title similarity
    similarity = title_similarity(
        event1.get('title', ''),
        event2.get('title', '')
    )

    if similarity < title_threshold:
        return False

    # Optionally check time
    if check_time:
        time1 = event1.get('time', '')
        time2 = event2.get('time', '')
        if time1 and time2 and time1 != time2:
            return False

    # Check location similarity
    loc1 = normalize_location(event1.get('location', ''))
    loc2 = normalize_location(event2.get('location', ''))

    if loc1 and loc2:
        loc_similarity = SequenceMatcher(None, loc1, loc2).ratio()
        if loc_similarity < 0.7:
            return False

    return True


def deduplicate_events(events: List[Dict],
                       prefer_source: str = None) -> List[Dict]:
    """
    Remove duplicate events from a list.

    Args:
        events: List of events to deduplicate
        prefer_source: Source ID to prefer when duplicates found

    Returns:
        Deduplicated list of events
    """
    if not events:
        return []

    # Sort by source preference if specified
    if prefer_source:
        events = sorted(
            events,
            key=lambda e: (0 if e.get('source') == prefer_source else 1)
        )

    seen_hashes: Set[str] = set()
    deduplicated: List[Dict] = []

    for event in events:
        event_hash = generate_event_hash(event)

        if event_hash in seen_hashes:
            continue

        # Check against all existing events for fuzzy duplicates
        is_dup = False
        for existing in deduplicated:
            if is_duplicate(event, existing):
                is_dup = True
                break

        if not is_dup:
            deduplicated.append(event)
            seen_hashes.add(event_hash)

    return deduplicated


def merge_duplicate_events(events: List[Dict]) -> List[Dict]:
    """
    Merge duplicate events, combining information from multiple sources.

    Args:
        events: List of events that may contain duplicates

    Returns:
        List of merged events
    """
    if not events:
        return []

    # Group potential duplicates
    groups: List[List[Dict]] = []
    used: Set[int] = set()

    for i, event in enumerate(events):
        if i in used:
            continue

        group = [event]
        used.add(i)

        for j, other in enumerate(events[i+1:], start=i+1):
            if j in used:
                continue
            if is_duplicate(event, other):
                group.append(other)
                used.add(j)

        groups.append(group)

    # Merge each group
    merged: List[Dict] = []
    for group in groups:
        if len(group) == 1:
            merged.append(group[0])
        else:
            merged.append(_merge_event_group(group))

    return merged


def _merge_event_group(events: List[Dict]) -> Dict:
    """
    Merge a group of duplicate events into one.

    Args:
        events: List of duplicate events

    Returns:
        Merged event
    """
    if not events:
        return {}

    # Start with the first event
    merged = events[0].copy()

    # Track all sources
    sources = [e.get('source') for e in events if e.get('source')]
    merged['sources'] = list(set(sources))

    # Collect all links
    links = [e.get('link') for e in events if e.get('link')]
    merged['all_links'] = list(set(links))

    # Use the longest description
    descriptions = [(len(e.get('description', '')), e.get('description', ''))
                    for e in events]
    descriptions.sort(reverse=True)
    if descriptions:
        merged['description'] = descriptions[0][1]

    # Merge tags
    all_tags = []
    for e in events:
        all_tags.extend(e.get('tags', []))
    merged['tags'] = list(set(all_tags))

    # Create merged ID
    merged['id'] = f"merged-{generate_event_hash(merged)[:12]}"

    return merged


def find_recurring_events(events: List[Dict],
                          min_occurrences: int = 2) -> List[Tuple[str, List[Dict]]]:
    """
    Find events that appear to be recurring.

    Args:
        events: List of events
        min_occurrences: Minimum occurrences to consider recurring

    Returns:
        List of (normalized_title, events) tuples for recurring events
    """
    # Group by normalized title
    title_groups: Dict[str, List[Dict]] = {}

    for event in events:
        norm_title = normalize_title(event.get('title', ''))
        if norm_title:
            if norm_title not in title_groups:
                title_groups[norm_title] = []
            title_groups[norm_title].append(event)

    # Filter to recurring events
    recurring = [
        (title, group) for title, group in title_groups.items()
        if len(group) >= min_occurrences
    ]

    # Sort by occurrence count
    recurring.sort(key=lambda x: len(x[1]), reverse=True)

    return recurring
