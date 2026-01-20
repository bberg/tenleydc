"""
Anacostia History Website
A Flask application documenting the history of Anacostia, Washington's first suburb
"""

from flask import Flask, render_template, abort, request
import markdown
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Site configuration
SITE_CONFIG = {
    "domain": "anacostiahub.com",
    "site_name": "Anacostia Almanac",
    "tagline": "History and community of Anacostia, DC",
    "region": "Southeast Washington DC"
}


# Configuration
CONTENT_DIR = Path(__file__).parent / 'content'
DATA_DIR = Path(__file__).parent / 'data'

# Navigation structure with groups
NAVIGATION = [
    # Main (no group - always visible)
    {'slug': 'overview', 'title': 'Overview', 'icon': 'home', 'group': None},
    {'slug': 'events', 'title': 'Events', 'icon': 'calendar', 'group': None},
    {'slug': 'map', 'title': 'Explore the Map', 'icon': 'map-marked-alt', 'group': None},

    # Community
    {'slug': 'schools', 'title': 'Schools', 'icon': 'school', 'group': 'Community'},
    {'slug': 'arts', 'title': 'Arts & Culture', 'icon': 'palette', 'group': 'Community'},
    {'slug': 'worship', 'title': 'Houses of Worship', 'icon': 'place-of-worship', 'group': 'Community'},
    {'slug': 'services', 'title': 'Public Services', 'icon': 'building-columns', 'group': 'Community'},
    {'slug': 'businesses', 'title': 'Local Businesses', 'icon': 'store', 'group': 'Community'},
    {'slug': 'dining', 'title': 'Dining Guide', 'icon': 'utensils', 'group': 'Community'},
    {'slug': 'neighborhood_guide', 'title': 'Neighborhood Guide', 'icon': 'compass', 'group': 'Community'},

    # Places
    {'slug': 'cedar_hill', 'title': 'Cedar Hill', 'icon': 'landmark', 'group': 'Places'},
    {'slug': 'barry_farm', 'title': 'Barry Farm', 'icon': 'building', 'group': 'Places'},
    {'slug': 'historic_anacostia', 'title': 'Historic Anacostia', 'icon': 'monument', 'group': 'Places'},
    {'slug': 'anacostia_park', 'title': 'Anacostia Park', 'icon': 'tree', 'group': 'Places'},
    {'slug': 'neighborhoods', 'title': 'Neighborhoods', 'icon': 'map', 'group': 'Places'},

    # History
    {'slug': 'timeline', 'title': 'Timeline', 'icon': 'clock', 'group': 'History'},
    {'slug': 'history', 'title': 'Full History', 'icon': 'book-open', 'group': 'History'},
    {'slug': 'frederick_douglass', 'title': 'Frederick Douglass', 'icon': 'user', 'group': 'History'},
    {'slug': 'civil_rights', 'title': 'Civil Rights Era', 'icon': 'fist-raised', 'group': 'History'},
    {'slug': 'landmarks', 'title': 'Landmarks', 'icon': 'landmark', 'group': 'History'},

    # Reference
    {'slug': 'demographics', 'title': 'Demographics', 'icon': 'users', 'group': 'Reference'},
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


def load_categories():
    """Load categories from JSON file"""
    file_path = DATA_DIR / 'categories.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('categories', [])


def load_events():
    """Load events from JSON file"""
    file_path = DATA_DIR / 'events.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('events', [])


def get_business_by_slug(slug):
    """Get a single business by its slug"""
    businesses = load_businesses()
    for business in businesses:
        if business.get('slug') == slug:
            return business
    return None


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
    title = 'Anacostia History'
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


@app.route('/businesses')
@app.route('/businesses/')
def business_directory():
    """Business directory main page"""
    businesses = load_businesses()
    categories = load_categories()

    category_filter = request.args.get('category')
    neighborhood_filter = request.args.get('neighborhood')

    if category_filter:
        businesses = [b for b in businesses if b.get('category') == category_filter]
    if neighborhood_filter:
        businesses = [b for b in businesses if b.get('neighborhood') == neighborhood_filter]

    businesses.sort(key=lambda x: (not x.get('featured', False), x.get('name', '').lower()))

    return render_template('page.html',
                         businesses=businesses,
                         categories=categories,
                         current_category=category_filter,
                         current_neighborhood=neighborhood_filter,
                         title='Local Businesses',
                         navigation=NAVIGATION,
                         current_page='businesses')


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

    return render_template('page.html',
                         events=upcoming,
                         categories=categories,
                         current_category=category_filter,
                         title='Events',
                         navigation=NAVIGATION,
                         current_page='events')


@app.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '').lower()

    results = []
    if query:
        for item in NAVIGATION:
            if item['slug'] in ['businesses', 'dining', 'events']:
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


@app.route('/map')
def interactive_map():
    """Interactive map page"""
    return render_template('page.html',
                         title='Interactive Map',
                         navigation=NAVIGATION,
                         current_page='map')


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
    app.run(debug=True, port=5089)
