"""Woodley Park Almanac
A Flask application documenting the history of Woodley Park, DC"""

from flask import Flask, render_template, abort, request
import markdown
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Site configuration
SITE_CONFIG = {
    "domain": "woodleyhub.com",
    "site_name": "Woodley Park Almanac",
    "tagline": "History and community of Woodley Park, DC",
    "region": "Northwest Washington DC"
}


# Configuration
CONTENT_DIR = Path(__file__).parent / 'content'
DATA_DIR = Path(__file__).parent / 'data'

# Navigation structure with groups
NAVIGATION = [
    # Main (no group - always visible)
    {'slug': 'overview', 'title': 'Overview', 'icon': 'home', 'group': None},
    {'slug': 'events', 'title': 'Events', 'icon': 'calendar', 'group': None},

    # Places
    {'slug': 'woodley-park', 'title': 'Woodley Park', 'icon': 'map-marker-alt', 'group': 'Places'},
    {'slug': 'national_zoo', 'title': 'National Zoo', 'icon': 'paw', 'group': 'Places'},
    {'slug': 'rock_creek', 'title': 'Rock Creek Park', 'icon': 'tree', 'group': 'Places'},
    {'slug': 'connecticut_avenue', 'title': 'Connecticut Avenue', 'icon': 'road', 'group': 'Places'},

    # History
    {'slug': 'timeline', 'title': 'Timeline', 'icon': 'clock', 'group': 'History'},
    {'slug': 'woodley_house', 'title': 'Woodley House', 'icon': 'home', 'group': 'History'},
    {'slug': 'wardman', 'title': 'Harry Wardman Era', 'icon': 'hard-hat', 'group': 'History'},
    {'slug': 'taft_bridge', 'title': 'Taft Bridge', 'icon': 'archway', 'group': 'History'},

    # Landmarks
    {'slug': 'kennedy_warren', 'title': 'Kennedy-Warren', 'icon': 'building', 'group': 'Landmarks'},
    {'slug': 'wardman_tower', 'title': 'Wardman Tower', 'icon': 'hotel', 'group': 'Landmarks'},
    {'slug': 'omni_shoreham', 'title': 'Omni Shoreham', 'icon': 'concierge-bell', 'group': 'Landmarks'},

    # Reference
    {'slug': 'resources', 'title': 'Resources', 'icon': 'book', 'group': 'Reference'},
    {'slug': 'about', 'title': 'About', 'icon': 'info-circle', 'group': 'Reference'},
]


# ============================================
# DATA LOADING UTILITIES
# ============================================

def load_businesses():
    """Load all businesses from JSON file"""
    file_path = DATA_DIR / 'businesses.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('businesses', [])


def load_events():
    """Load events from JSON file"""
    file_path = DATA_DIR / 'events.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('events', [])


def load_schools():
    """Load schools from JSON file"""
    file_path = DATA_DIR / 'schools.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('schools', [])


def get_featured_businesses(limit=4):
    """Get featured businesses for homepage"""
    businesses = load_businesses()
    today = datetime.now().strftime('%Y-%m-%d')
    featured = [
        b for b in businesses
        if b.get('featured') and (not b.get('featured_until') or b.get('featured_until') >= today)
    ]
    return featured[:limit]


def get_featured_events(limit=3):
    """Get featured upcoming events, sorted by date"""
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [
        e for e in events
        if e.get('featured') and (e.get('date', '') >= today or e.get('end_date', '') >= today)
    ]
    upcoming.sort(key=lambda x: x.get('date', ''))
    return upcoming[:limit]


def get_upcoming_events(limit=10):
    """Get upcoming events sorted by date"""
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [
        e for e in events
        if e.get('date', '') >= today or e.get('end_date', '') >= today
    ]
    upcoming.sort(key=lambda x: x.get('date', ''))
    return upcoming[:limit]


def load_markdown_content(slug):
    """Load and convert markdown content to HTML"""
    file_path = CONTENT_DIR / f'{slug}.md'

    if not file_path.exists():
        return None, None, None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert markdown to HTML with extensions
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'toc',
        'attr_list',
        'def_list',
        'footnotes'
    ])

    html_content = md.convert(content)
    toc = md.toc if hasattr(md, 'toc') else ''

    # Extract title from first H1
    lines = content.split('\n')
    title = 'Woodley Park Almanac'
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    return html_content, title, toc


# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    """Home page with overview"""
    content, title, toc = load_markdown_content('overview')
    if content is None:
        abort(404)

    featured_businesses = get_featured_businesses(4)
    featured_events = get_featured_events(3)

    return render_template('home.html',
                         content=content,
                         title=title,
                         toc=toc,
                         navigation=NAVIGATION,
                         current_page='overview',
                         featured_businesses=featured_businesses,
                         featured_events=featured_events)


@app.route('/page/<slug>')
def page(slug):
    """Dynamic page routing for all content pages"""
    content, title, toc = load_markdown_content(slug)

    if content is None:
        abort(404)

    return render_template('page.html',
                         content=content,
                         title=title,
                         toc=toc,
                         navigation=NAVIGATION,
                         current_page=slug)


# ============================================
# EVENTS ROUTES
# ============================================

@app.route('/events')
@app.route('/events/')
def events_page():
    """Events listing page"""
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')

    category_filter = request.args.get('category')
    if category_filter:
        events = [e for e in events if e.get('category') == category_filter]

    upcoming = [e for e in events if e.get('date', '') >= today or e.get('end_date', '') >= today]
    upcoming.sort(key=lambda x: x.get('date', ''))

    all_events = load_events()
    categories = list(set(e.get('category') for e in all_events if e.get('category')))
    categories.sort()

    return render_template('events.html',
                         events=upcoming,
                         categories=categories,
                         current_category=category_filter,
                         title='Events',
                         navigation=NAVIGATION,
                         current_page='events')


# ============================================
# SEARCH
# ============================================

@app.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '').lower()

    results = []
    if query:
        for item in NAVIGATION:
            if item['slug'] in ['businesses', 'events']:
                continue
            file_path = CONTENT_DIR / f"{item['slug']}.md"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query in content:
                        idx = content.find(query)
                        start = max(0, idx - 100)
                        end = min(len(content), idx + 100)
                        snippet = content[start:end]
                        if start > 0:
                            snippet = '...' + snippet
                        if end < len(content):
                            snippet = snippet + '...'

                        results.append({
                            'title': item['title'],
                            'slug': item['slug'],
                            'snippet': snippet,
                            'type': 'page'
                        })

        businesses = load_businesses()
        for business in businesses:
            searchable = f"{business.get('name', '')} {business.get('description', '')} {business.get('tags', [])}".lower()
            if query in searchable:
                results.append({
                    'title': business.get('name'),
                    'slug': f"business/{business.get('slug')}",
                    'snippet': business.get('description', '')[:150] + '...',
                    'type': 'business'
                })

    return render_template('search.html',
                         query=query,
                         results=results,
                         navigation=NAVIGATION,
                         current_page='search')


@app.route('/about')
def about():
    """About page"""
    content, title, toc = load_markdown_content('about')
    if content is None:
        abort(404)
    return render_template('page.html',
                         content=content,
                         title=title,
                         toc=toc,
                         navigation=NAVIGATION,
                         current_page='about')


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html',
                         navigation=NAVIGATION,
                         current_page=None), 404


if __name__ == '__main__':
    app.run(debug=True, port=5003)
