"""
Configuration and constants for Tennally's Almanac scrapers
"""

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONTENT_DIR = PROJECT_ROOT / "content"

# Scraper settings
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_DELAY = 5  # seconds

# User agent for requests
USER_AGENT = "TennallysAlmanac/1.0 (Community Event Aggregator; https://tennallysalmanac.com)"

# Rate limiting (requests per minute per domain)
RATE_LIMIT = 10

# Event categories
CATEGORIES = {
    "literary": "Literary & Books",
    "family": "Family & Children",
    "music": "Music & Performance",
    "art": "Art & Exhibitions",
    "community": "Community Events",
    "food": "Food & Dining",
    "outdoors": "Outdoors & Nature",
    "education": "Education & Workshops",
    "sports": "Sports & Recreation",
    "civic": "Civic & Government",
    "religious": "Religious & Spiritual",
    "farmers-market": "Farmers Markets",
    "other": "Other Events"
}

# Geographic boundaries for AU Park / Tenleytown area
# Approximate bounding box
GEO_BOUNDS = {
    "north": 38.9600,
    "south": 38.9350,
    "east": -77.0700,
    "west": -77.1000
}

# Key locations in the neighborhood
NEIGHBORHOOD_LOCATIONS = [
    "Tenleytown",
    "AU Park",
    "American University Park",
    "Friendship Heights",
    "Wisconsin Avenue NW",
    "Nebraska Avenue NW",
    "Massachusetts Avenue NW",
    "Tenley-Friendship Library",
    "Politics and Prose",
    "Janney Elementary",
    "Wilson High School",
    "Deal Middle School",
    "Fort Reno",
    "Turtle Park",
    "Guy Mason Recreation Center"
]

# Source configurations (also stored in data/sources.json)
DEFAULT_SOURCES = {
    "politics-prose": {
        "id": "politics-prose",
        "name": "Politics and Prose",
        "url": "https://www.politics-prose.com/events",
        "scraper": "politics_prose",
        "schedule": "weekly",
        "default_category": "literary",
        "active": True
    },
    "dc-library-tenley": {
        "id": "dc-library-tenley",
        "name": "Tenley-Friendship Library",
        "url": "https://www.dclibrary.org/node/69141/events",
        "scraper": "dc_library",
        "schedule": "weekly",
        "default_category": "family",
        "active": True
    }
}

# Output formats
OUTPUT_FORMATS = ["json", "markdown", "ical"]

# Date/time formats
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
