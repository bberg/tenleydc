"""Vienna Almanac
A Flask application documenting the history of Vienna, Virginia"""

from flask import Flask, render_template, abort, request
import markdown
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Site configuration
SITE_CONFIG = {
    "domain": "viennalocal.com",
    "site_name": "Vienna Almanac",
    "tagline": "History and community of Vienna, Virginia",
    "region": "Fairfax County, Virginia"
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
    {'slug': 'church_street', 'title': 'Church Street', 'icon': 'road', 'group': 'Places'},
    {'slug': 'town_green', 'title': 'Town Green', 'icon': 'tree', 'group': 'Places'},
    {'slug': 'wolf_trap', 'title': 'Wolf Trap', 'icon': 'music', 'group': 'Places'},
    {'slug': 'freeman_house', 'title': 'Freeman House', 'icon': 'house', 'group': 'Places'},
    {'slug': 'wnt_trail', 'title': 'W&OD Trail', 'icon': 'bicycle', 'group': 'Places'},
    {'slug': 'neighborhoods', 'title': 'Neighborhoods', 'icon': 'map', 'group': 'Places'},

    # History
    {'slug': 'timeline', 'title': 'Timeline', 'icon': 'clock', 'group': 'History'},
    {'slug': 'history', 'title': 'Full History', 'icon': 'book', 'group': 'History'},
    {'slug': 'civil_war', 'title': 'Civil War History', 'icon': 'flag', 'group': 'History'},
    {'slug': 'railroad', 'title': 'Railroad Era', 'icon': 'train', 'group': 'History'},
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


def load_schools():
    """Load schools from JSON file"""
    file_path = DATA_DIR / 'schools.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('schools', [])


def load_arts():
    """Load arts institutions from JSON file"""
    file_path = DATA_DIR / 'arts.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('arts_institutions', [])


def load_religious():
    """Load religious institutions from JSON file"""
    file_path = DATA_DIR / 'religious.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('institutions', [])


def load_services():
    """Load public services from JSON file"""
    file_path = DATA_DIR / 'services.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('services', [])


def load_pending_events():
    """Load pending scraped events"""
    file_path = DATA_DIR / 'scraped' / 'events_pending.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('events', [])


def load_event_sources():
    """Load event source configuration"""
    file_path = DATA_DIR / 'sources.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('event_sources', [])


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


def get_businesses_by_category(category):
    """Get businesses filtered by category"""
    businesses = load_businesses()
    return [b for b in businesses if b.get('category') == category]


def get_businesses_by_subcategory(subcategory):
    """Get businesses filtered by subcategory"""
    businesses = load_businesses()
    return [b for b in businesses if b.get('subcategory') == subcategory]


def get_featured_events(limit=3):
    """Get featured upcoming events, sorted by date"""
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [
        e for e in events
        if e.get('featured') and (e.get('date', '') >= today or e.get('end_date', '') >= today)
    ]
    # Sort by date to show soonest events first
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
    # Sort by date
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
    title = 'Vienna Almanac'
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

    # Get featured content for homepage
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
# BUSINESS DIRECTORY ROUTES
# ============================================

@app.route('/businesses')
@app.route('/businesses/')
def business_directory():
    """Business directory main page"""
    businesses = load_businesses()
    categories = load_categories()

    # Get query parameters for filtering
    category_filter = request.args.get('category')
    neighborhood_filter = request.args.get('neighborhood')

    if category_filter:
        businesses = [b for b in businesses if b.get('category') == category_filter]
    if neighborhood_filter:
        businesses = [b for b in businesses if b.get('neighborhood') == neighborhood_filter]

    # Sort: featured first, then alphabetically
    businesses.sort(key=lambda x: (not x.get('featured', False), x.get('name', '').lower()))

    return render_template('business-directory.html',
                         businesses=businesses,
                         categories=categories,
                         current_category=category_filter,
                         current_neighborhood=neighborhood_filter,
                         title='Local Businesses',
                         navigation=NAVIGATION,
                         current_page='businesses')


@app.route('/business/<slug>')
def business_profile(slug):
    """Individual business profile page"""
    business = get_business_by_slug(slug)
    if not business:
        abort(404)

    # Get related businesses (same category, excluding current)
    all_businesses = load_businesses()
    related = [
        b for b in all_businesses
        if b.get('category') == business.get('category') and b.get('slug') != slug
    ][:4]

    return render_template('business-profile.html',
                         business=business,
                         related_businesses=related,
                         title=business.get('name'),
                         navigation=NAVIGATION,
                         current_page='businesses')


@app.route('/dining')
@app.route('/dining/')
def dining_guide():
    """Dining guide - restaurants, cafes, bars"""
    businesses = load_businesses()
    categories = load_categories()

    # Filter to dining category
    dining_businesses = [b for b in businesses if b.get('category') == 'dining']

    # Get subcategory filter
    subcategory_filter = request.args.get('type')
    if subcategory_filter:
        dining_businesses = [b for b in dining_businesses if b.get('subcategory') == subcategory_filter]

    # Sort: featured first, then alphabetically
    dining_businesses.sort(key=lambda x: (not x.get('featured', False), x.get('name', '').lower()))

    # Get dining subcategories
    dining_category = next((c for c in categories if c.get('id') == 'dining'), None)
    subcategories = dining_category.get('subcategories', []) if dining_category else []

    return render_template('dining.html',
                         businesses=dining_businesses,
                         subcategories=subcategories,
                         current_type=subcategory_filter,
                         title='Dining Guide',
                         navigation=NAVIGATION,
                         current_page='dining')


# ============================================
# EVENTS ROUTES
# ============================================

@app.route('/events')
@app.route('/events/')
def events_page():
    """Events listing page"""
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')

    # Filter by category if provided
    category_filter = request.args.get('category')
    if category_filter:
        events = [e for e in events if e.get('category') == category_filter]

    # Separate into upcoming and past
    upcoming = [e for e in events if e.get('date', '') >= today or e.get('end_date', '') >= today]
    upcoming.sort(key=lambda x: x.get('date', ''))

    # Get unique categories for filter
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
# SCHOOLS
# ============================================

@app.route('/schools')
@app.route('/schools/')
def schools_page():
    """Schools directory page"""
    schools = load_schools()

    # Filter by type if provided
    type_filter = request.args.get('type')
    level_filter = request.args.get('level')

    if type_filter:
        schools = [s for s in schools if s.get('type') == type_filter]
    if level_filter:
        schools = [s for s in schools if s.get('level') == level_filter]

    # Sort: featured first, then alphabetically
    schools.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('schools.html',
                         schools=schools,
                         current_type=type_filter,
                         current_level=level_filter,
                         title='Schools',
                         navigation=NAVIGATION,
                         current_page='schools')


@app.route('/school/<slug>')
def school_profile(slug):
    """Individual school profile page"""
    schools = load_schools()
    school = next((s for s in schools if s.get('slug') == slug), None)

    if not school:
        return render_template('404.html', navigation=NAVIGATION), 404

    # Get related schools (same neighborhood or type)
    related = [s for s in schools
               if s.get('slug') != slug and
               (s.get('neighborhood') == school.get('neighborhood') or
                s.get('type') == school.get('type'))][:3]

    return render_template('school-profile.html',
                         school=school,
                         related_schools=related,
                         title=school.get('name'),
                         navigation=NAVIGATION,
                         current_page='schools')


# ============================================
# ARTS & CULTURE
# ============================================

@app.route('/arts')
@app.route('/arts/')
def arts_page():
    """Arts & Culture directory page"""
    institutions = load_arts()

    # Filter by type if provided
    type_filter = request.args.get('type')
    if type_filter:
        institutions = [i for i in institutions if i.get('type') == type_filter]

    # Sort: featured first, then alphabetically
    institutions.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('arts.html',
                         institutions=institutions,
                         current_type=type_filter,
                         title='Arts & Culture',
                         navigation=NAVIGATION,
                         current_page='arts')


@app.route('/arts/<slug>')
def arts_profile(slug):
    """Individual arts venue profile page"""
    institutions = load_arts()
    venue = next((i for i in institutions if i.get('slug') == slug), None)

    if not venue:
        return render_template('404.html', navigation=NAVIGATION), 404

    return render_template('arts-profile.html',
                         venue=venue,
                         title=venue.get('name'),
                         navigation=NAVIGATION,
                         current_page='arts')


# ============================================
# HOUSES OF WORSHIP
# ============================================

@app.route('/worship')
@app.route('/worship/')
def worship_page():
    """Houses of Worship directory page"""
    institutions = load_religious()

    # Filter by type if provided
    type_filter = request.args.get('type')
    if type_filter:
        institutions = [i for i in institutions if i.get('type') == type_filter]

    # Sort: featured first, then alphabetically
    institutions.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('worship.html',
                         institutions=institutions,
                         current_type=type_filter,
                         title='Houses of Worship',
                         navigation=NAVIGATION,
                         current_page='worship')


@app.route('/worship/<slug>')
def worship_profile(slug):
    """Individual house of worship profile page"""
    institutions = load_religious()
    institution = next((i for i in institutions if i.get('slug') == slug), None)

    if not institution:
        return render_template('404.html', navigation=NAVIGATION), 404

    return render_template('worship-profile.html',
                         institution=institution,
                         title=institution.get('name'),
                         navigation=NAVIGATION,
                         current_page='worship')


# ============================================
# PUBLIC SERVICES
# ============================================

@app.route('/services')
@app.route('/services/')
def services_page():
    """Public Services directory page"""
    services = load_services()

    # Filter by type if provided
    type_filter = request.args.get('type')
    if type_filter:
        services = [s for s in services if s.get('type') == type_filter]

    # Sort: featured first, then alphabetically
    services.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('services.html',
                         services=services,
                         current_type=type_filter,
                         title='Public Services',
                         navigation=NAVIGATION,
                         current_page='services')


@app.route('/services/<slug>')
def services_profile(slug):
    """Individual public service profile page"""
    services = load_services()
    service = next((s for s in services if s.get('slug') == slug), None)

    if not service:
        return render_template('404.html', navigation=NAVIGATION), 404

    return render_template('services-profile.html',
                         service=service,
                         title=service.get('name'),
                         navigation=NAVIGATION,
                         current_page='services')


# ============================================
# SEARCH
# ============================================

@app.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '').lower()

    results = []
    if query:
        # Search markdown content
        for item in NAVIGATION:
            # Skip non-content pages
            if item['slug'] in ['businesses', 'dining', 'events']:
                continue
            file_path = CONTENT_DIR / f"{item['slug']}.md"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query in content:
                        # Find a relevant snippet
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

        # Search businesses
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
    return render_template('map.html',
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
    app.run(debug=True, port=5091)
