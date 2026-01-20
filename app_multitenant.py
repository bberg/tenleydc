"""
Multi-Tenant DMV Neighborhood History Sites
A single Flask application serving 16 neighborhood sites based on domain.

Each site's content, data, and templates live in sites/{site}/ directories.
The app detects the domain and serves the appropriate site.

Usage:
  python app_multitenant.py                    # Runs on localhost:5000, defaults to tenleytown
  SITE_OVERRIDE=brightwood python app_multitenant.py  # Force a specific site for testing
"""

from flask import Flask, render_template, abort, request, g, send_from_directory, redirect
from jinja2 import FileSystemLoader, ChoiceLoader
import markdown
import json
import os
from pathlib import Path
from datetime import datetime
from functools import wraps

# ============================================
# SITE CONFIGURATION
# ============================================

# Domain to site directory mapping
DOMAIN_TO_SITE = {
    # DC Sites (10)
    "tenleydc.com": "tenleytown",
    "www.tenleydc.com": "tenleytown",
    "brightwooddc.com": "brightwood",
    "www.brightwooddc.com": "brightwood",
    "kaloramadc.com": "kalorama",
    "www.kaloramadc.com": "kalorama",
    "cheights.com": "columbia-heights",
    "www.cheights.com": "columbia-heights",
    "hstreethub.com": "h-street",
    "www.hstreethub.com": "h-street",
    "swdclocal.com": "sw-waterfront",
    "www.swdclocal.com": "sw-waterfront",
    "anacostiahub.com": "anacostia",
    "www.anacostiahub.com": "anacostia",
    "shepherdparkdc.com": "shepherd-park",
    "www.shepherdparkdc.com": "shepherd-park",
    "gloverdc.com": "glover-park",
    "www.gloverdc.com": "glover-park",
    "woodleyhub.com": "woodley-park",
    "www.woodleyhub.com": "woodley-park",
    # Maryland Sites (3)
    "collegeparkhub.com": "college-park",
    "www.collegeparkhub.com": "college-park",
    "hyattsvillehub.com": "hyattsville",
    "www.hyattsvillehub.com": "hyattsville",
    "potomacspot.com": "potomac",
    "www.potomacspot.com": "potomac",
    # Virginia Sites (3)
    "fallschurchhub.com": "falls-church",
    "www.fallschurchhub.com": "falls-church",
    "viennalocal.com": "vienna",
    "www.viennalocal.com": "vienna",
    "delrayva.com": "del-ray",
    "www.delrayva.com": "del-ray",
    # Local development
    "localhost": "tenleytown",
    "127.0.0.1": "tenleytown",
}

# Site metadata (for GA, SEO, etc.)
SITE_METADATA = {
    "tenleytown": {
        "ga_id": "G-FWWPBGYKR1",
        "site_name": "Tenley DC",
        "tagline": "Upper Northwest DC",
    },
    "brightwood": {
        "ga_id": "",
        "site_name": "Brightwood Almanac",
        "tagline": "History and community of Brightwood, DC",
    },
    "kalorama": {
        "ga_id": "",
        "site_name": "Kalorama Almanac",
        "tagline": "History and community of Kalorama, DC",
    },
    "columbia-heights": {
        "ga_id": "",
        "site_name": "Columbia Heights Almanac",
        "tagline": "History and community of Columbia Heights, DC",
    },
    "h-street": {
        "ga_id": "",
        "site_name": "H Street Almanac",
        "tagline": "History and community of the H Street Corridor",
    },
    "sw-waterfront": {
        "ga_id": "",
        "site_name": "SW Waterfront Almanac",
        "tagline": "History and community of Southwest DC",
    },
    "anacostia": {
        "ga_id": "",
        "site_name": "Anacostia Almanac",
        "tagline": "History and community of Anacostia, DC",
    },
    "shepherd-park": {
        "ga_id": "",
        "site_name": "Shepherd Park Almanac",
        "tagline": "History and community of Shepherd Park, DC",
    },
    "glover-park": {
        "ga_id": "",
        "site_name": "Glover Park Almanac",
        "tagline": "History and community of Glover Park, DC",
    },
    "woodley-park": {
        "ga_id": "",
        "site_name": "Woodley Park Almanac",
        "tagline": "History and community of Woodley Park, DC",
    },
    "college-park": {
        "ga_id": "",
        "site_name": "College Park Almanac",
        "tagline": "History and community of College Park, Maryland",
    },
    "hyattsville": {
        "ga_id": "",
        "site_name": "Hyattsville Almanac",
        "tagline": "History and community of Hyattsville, Maryland",
    },
    "potomac": {
        "ga_id": "",
        "site_name": "Potomac Almanac",
        "tagline": "History and community of Potomac, Maryland",
    },
    "falls-church": {
        "ga_id": "",
        "site_name": "Falls Church Almanac",
        "tagline": "History and community of Falls Church, Virginia",
    },
    "vienna": {
        "ga_id": "",
        "site_name": "Vienna Almanac",
        "tagline": "History and community of Vienna, Virginia",
    },
    "del-ray": {
        "ga_id": "",
        "site_name": "Del Ray Almanac",
        "tagline": "History and community of Del Ray, Alexandria",
    },
}

# Base paths
BASE_DIR = Path(__file__).parent
SITES_DIR = BASE_DIR / 'sites'

# Default site for localhost/unknown domains
DEFAULT_SITE = os.environ.get('SITE_OVERRIDE', 'tenleytown')


# ============================================
# FLASK APP SETUP
# ============================================

app = Flask(__name__,
            template_folder='sites/tenleytown/templates',  # Default, overridden per-request
            static_folder='sites/tenleytown/static')       # Default, overridden per-request


def get_site_from_host():
    """Determine which site to serve based on the request host."""
    # Check for environment override (for local testing)
    if os.environ.get('SITE_OVERRIDE'):
        return os.environ.get('SITE_OVERRIDE')

    # Get host without port
    host = request.host.split(':')[0].lower()

    # Look up site from domain mapping
    site = DOMAIN_TO_SITE.get(host, DEFAULT_SITE)
    return site


def get_site_paths(site):
    """Get the content and data paths for a site."""
    site_dir = SITES_DIR / site
    return {
        'site_dir': site_dir,
        'content_dir': site_dir / 'content',
        'data_dir': site_dir / 'data',
        'template_dir': site_dir / 'templates',
        'static_dir': site_dir / 'static',
    }


@app.before_request
def before_request():
    """Set up site-specific context before each request."""
    g.site = get_site_from_host()
    g.paths = get_site_paths(g.site)
    g.metadata = SITE_METADATA.get(g.site, SITE_METADATA[DEFAULT_SITE])

    # Update Jinja loader to use the site's templates
    site_template_dir = str(g.paths['template_dir'])
    app.jinja_loader = FileSystemLoader(site_template_dir)


# ============================================
# STATIC FILE SERVING (per-site)
# ============================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the current site's static directory."""
    return send_from_directory(str(g.paths['static_dir']), filename)


# ============================================
# NAVIGATION LOADING
# ============================================

def load_navigation():
    """Load navigation from site's app.py or use default."""
    # Try to load from site's nav.json if it exists
    nav_file = g.paths['site_dir'] / 'nav.json'
    if nav_file.exists():
        with open(nav_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Default navigation structure
    return [
        {'slug': 'overview', 'title': 'Overview', 'icon': 'home', 'group': None},
        {'slug': 'events', 'title': 'Events', 'icon': 'calendar', 'group': None},
        {'slug': 'map', 'title': 'Explore the Map', 'icon': 'map-marked-alt', 'group': None},
        {'slug': 'schools', 'title': 'Schools', 'icon': 'school', 'group': 'Community'},
        {'slug': 'arts', 'title': 'Arts & Culture', 'icon': 'palette', 'group': 'Community'},
        {'slug': 'worship', 'title': 'Houses of Worship', 'icon': 'place-of-worship', 'group': 'Community'},
        {'slug': 'services', 'title': 'Public Services', 'icon': 'building-columns', 'group': 'Community'},
        {'slug': 'businesses', 'title': 'Local Businesses', 'icon': 'store', 'group': 'Community'},
        {'slug': 'dining', 'title': 'Dining Guide', 'icon': 'utensils', 'group': 'Community'},
        {'slug': 'neighborhood_guide', 'title': 'Neighborhood Guide', 'icon': 'compass', 'group': 'Community'},
        {'slug': 'timeline', 'title': 'Timeline', 'icon': 'clock', 'group': 'History'},
        {'slug': 'landmarks', 'title': 'Landmarks', 'icon': 'landmark', 'group': 'History'},
        {'slug': 'demographics', 'title': 'Demographics', 'icon': 'users', 'group': 'Reference'},
        {'slug': 'resources', 'title': 'Resources', 'icon': 'book', 'group': 'Reference'},
        {'slug': 'about', 'title': 'About', 'icon': 'info-circle', 'group': 'Reference'},
    ]


# ============================================
# DATA LOADING UTILITIES
# ============================================

def load_json_data(filename, key=None):
    """Load JSON data from the current site's data directory."""
    file_path = g.paths['data_dir'] / filename
    if not file_path.exists():
        return [] if key else {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get(key, []) if key else data


def load_businesses():
    return load_json_data('businesses.json', 'businesses')


def load_categories():
    return load_json_data('categories.json', 'categories')


def load_events():
    return load_json_data('events.json', 'events')


def load_schools():
    return load_json_data('schools.json', 'schools')


def load_arts():
    return load_json_data('arts.json', 'arts_institutions')


def load_religious():
    return load_json_data('religious.json', 'institutions')


def load_services():
    return load_json_data('services.json', 'services')


def load_pending_events():
    file_path = g.paths['data_dir'] / 'scraped' / 'events_pending.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('events', [])


def load_event_sources():
    return load_json_data('sources.json', 'event_sources')


def get_business_by_slug(slug):
    businesses = load_businesses()
    for business in businesses:
        if business.get('slug') == slug:
            return business
    return None


def get_featured_businesses(limit=4):
    businesses = load_businesses()
    today = datetime.now().strftime('%Y-%m-%d')
    featured = [
        b for b in businesses
        if b.get('featured') and (not b.get('featured_until') or b.get('featured_until') >= today)
    ]
    return featured[:limit]


def get_businesses_by_category(category):
    businesses = load_businesses()
    return [b for b in businesses if b.get('category') == category]


def get_featured_events(limit=3):
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [
        e for e in events
        if e.get('featured') and (e.get('date', '') >= today or e.get('end_date', '') >= today)
    ]
    upcoming.sort(key=lambda x: x.get('date', ''))
    return upcoming[:limit]


def get_upcoming_events(limit=10):
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = [
        e for e in events
        if e.get('date', '') >= today or e.get('end_date', '') >= today
    ]
    upcoming.sort(key=lambda x: x.get('date', ''))
    return upcoming[:limit]


def load_markdown_content(slug):
    """Load and convert markdown content to HTML."""
    file_path = g.paths['content_dir'] / f'{slug}.md'

    if not file_path.exists():
        return None, None, None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

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

    lines = content.split('\n')
    title = g.metadata.get('site_name', 'Neighborhood History')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    return html_content, title, toc


# ============================================
# TEMPLATE CONTEXT
# ============================================

@app.context_processor
def inject_site_context():
    """Inject site-specific variables into all templates."""
    return {
        'site': g.site,
        'site_metadata': g.metadata,
        'ga_id': g.metadata.get('ga_id', ''),
    }


# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    content, title, toc = load_markdown_content('overview')
    if content is None:
        abort(404)

    featured_businesses = get_featured_businesses(4)
    featured_events = get_featured_events(3)
    navigation = load_navigation()

    return render_template('home.html',
                         content=content,
                         title=title,
                         toc=toc,
                         navigation=navigation,
                         current_page='overview',
                         featured_businesses=featured_businesses,
                         featured_events=featured_events)


@app.route('/page/<slug>')
def page(slug):
    content, title, toc = load_markdown_content(slug)
    navigation = load_navigation()

    if content is None:
        abort(404)

    return render_template('page.html',
                         content=content,
                         title=title,
                         toc=toc,
                         navigation=navigation,
                         current_page=slug)


# ============================================
# BUSINESS DIRECTORY ROUTES
# ============================================

@app.route('/businesses')
@app.route('/businesses/')
def business_directory():
    businesses = load_businesses()
    categories = load_categories()
    navigation = load_navigation()

    category_filter = request.args.get('category')
    neighborhood_filter = request.args.get('neighborhood')

    if category_filter:
        businesses = [b for b in businesses if b.get('category') == category_filter]
    if neighborhood_filter:
        businesses = [b for b in businesses if b.get('neighborhood') == neighborhood_filter]

    businesses.sort(key=lambda x: (not x.get('featured', False), x.get('name', '').lower()))

    return render_template('business-directory.html',
                         businesses=businesses,
                         categories=categories,
                         current_category=category_filter,
                         current_neighborhood=neighborhood_filter,
                         title='Local Businesses',
                         navigation=navigation,
                         current_page='businesses')


@app.route('/business/<slug>')
def business_profile(slug):
    business = get_business_by_slug(slug)
    navigation = load_navigation()

    if not business:
        abort(404)

    all_businesses = load_businesses()
    related = [
        b for b in all_businesses
        if b.get('category') == business.get('category') and b.get('slug') != slug
    ][:4]

    return render_template('business-profile.html',
                         business=business,
                         related_businesses=related,
                         title=business.get('name'),
                         navigation=navigation,
                         current_page='businesses')


@app.route('/dining')
@app.route('/dining/')
def dining_guide():
    businesses = load_businesses()
    categories = load_categories()
    navigation = load_navigation()

    dining_businesses = [b for b in businesses if b.get('category') == 'dining']

    subcategory_filter = request.args.get('type')
    if subcategory_filter:
        dining_businesses = [b for b in dining_businesses if b.get('subcategory') == subcategory_filter]

    dining_businesses.sort(key=lambda x: (not x.get('featured', False), x.get('name', '').lower()))

    dining_category = next((c for c in categories if c.get('id') == 'dining'), None)
    subcategories = dining_category.get('subcategories', []) if dining_category else []

    return render_template('dining.html',
                         businesses=dining_businesses,
                         subcategories=subcategories,
                         current_type=subcategory_filter,
                         title='Dining Guide',
                         navigation=navigation,
                         current_page='dining')


# ============================================
# EVENTS ROUTES
# ============================================

@app.route('/events')
@app.route('/events/')
def events_page():
    events = load_events()
    today = datetime.now().strftime('%Y-%m-%d')
    navigation = load_navigation()

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
                         navigation=navigation,
                         current_page='events')


# ============================================
# SCHOOLS
# ============================================

@app.route('/schools')
@app.route('/schools/')
def schools_page():
    schools = load_schools()
    navigation = load_navigation()

    type_filter = request.args.get('type')
    level_filter = request.args.get('level')

    if type_filter:
        schools = [s for s in schools if s.get('type') == type_filter]
    if level_filter:
        schools = [s for s in schools if s.get('level') == level_filter]

    schools.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('schools.html',
                         schools=schools,
                         current_type=type_filter,
                         current_level=level_filter,
                         title='Schools',
                         navigation=navigation,
                         current_page='schools')


@app.route('/school/<slug>')
def school_profile(slug):
    schools = load_schools()
    navigation = load_navigation()
    school = next((s for s in schools if s.get('slug') == slug), None)

    if not school:
        return render_template('404.html', navigation=navigation), 404

    related = [s for s in schools
               if s.get('slug') != slug and
               (s.get('neighborhood') == school.get('neighborhood') or
                s.get('type') == school.get('type'))][:3]

    return render_template('school-profile.html',
                         school=school,
                         related_schools=related,
                         title=school.get('name'),
                         navigation=navigation,
                         current_page='schools')


# ============================================
# ARTS & CULTURE
# ============================================

@app.route('/arts')
@app.route('/arts/')
def arts_page():
    institutions = load_arts()
    navigation = load_navigation()

    type_filter = request.args.get('type')
    if type_filter:
        institutions = [i for i in institutions if i.get('type') == type_filter]

    institutions.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('arts.html',
                         institutions=institutions,
                         current_type=type_filter,
                         title='Arts & Culture',
                         navigation=navigation,
                         current_page='arts')


@app.route('/arts/<slug>')
def arts_profile(slug):
    institutions = load_arts()
    navigation = load_navigation()
    venue = next((i for i in institutions if i.get('slug') == slug), None)

    if not venue:
        return render_template('404.html', navigation=navigation), 404

    return render_template('arts-profile.html',
                         venue=venue,
                         title=venue.get('name'),
                         navigation=navigation,
                         current_page='arts')


# ============================================
# HOUSES OF WORSHIP
# ============================================

@app.route('/worship')
@app.route('/worship/')
def worship_page():
    institutions = load_religious()
    navigation = load_navigation()

    type_filter = request.args.get('type')
    if type_filter:
        institutions = [i for i in institutions if i.get('type') == type_filter]

    institutions.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('worship.html',
                         institutions=institutions,
                         current_type=type_filter,
                         title='Houses of Worship',
                         navigation=navigation,
                         current_page='worship')


@app.route('/worship/<slug>')
def worship_profile(slug):
    institutions = load_religious()
    navigation = load_navigation()
    institution = next((i for i in institutions if i.get('slug') == slug), None)

    if not institution:
        return render_template('404.html', navigation=navigation), 404

    return render_template('worship-profile.html',
                         institution=institution,
                         title=institution.get('name'),
                         navigation=navigation,
                         current_page='worship')


# ============================================
# PUBLIC SERVICES
# ============================================

@app.route('/services')
@app.route('/services/')
def services_page():
    services = load_services()
    navigation = load_navigation()

    type_filter = request.args.get('type')
    if type_filter:
        services = [s for s in services if s.get('type') == type_filter]

    services.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('services.html',
                         services=services,
                         current_type=type_filter,
                         title='Public Services',
                         navigation=navigation,
                         current_page='services')


@app.route('/services/<slug>')
def services_profile(slug):
    services = load_services()
    navigation = load_navigation()
    service = next((s for s in services if s.get('slug') == slug), None)

    if not service:
        return render_template('404.html', navigation=navigation), 404

    return render_template('services-profile.html',
                         service=service,
                         title=service.get('name'),
                         navigation=navigation,
                         current_page='services')


# ============================================
# ADMIN - Event Review
# ============================================

@app.route('/admin/review/events')
def admin_review_events():
    pending_events = load_pending_events()
    navigation = load_navigation()

    return render_template('admin/review_events.html',
                         pending_events=pending_events,
                         title='Review Events',
                         navigation=navigation,
                         current_page='admin')


@app.route('/admin/review/approve', methods=['POST'])
def admin_approve_event():
    return redirect('/admin/review/events')


@app.route('/admin/review/reject', methods=['POST'])
def admin_reject_event():
    return redirect('/admin/review/events')


@app.route('/admin/scraper-status')
def admin_scraper_status():
    sources = load_event_sources()
    navigation = load_navigation()

    for source in sources:
        source['enabled'] = source.get('enabled', True)

    return render_template('admin/scraper_status.html',
                         sources=sources,
                         title='Scraper Status',
                         navigation=navigation,
                         current_page='admin')


@app.route('/admin/scrape/run', methods=['POST'])
def admin_run_scrapers():
    return redirect('/admin/scraper-status')


@app.route('/admin/scrape/run/<source_id>', methods=['POST'])
def admin_run_single_scraper(source_id):
    return redirect('/admin/scraper-status')


@app.route('/admin/scrape/toggle/<source_id>', methods=['POST'])
def admin_toggle_source(source_id):
    return redirect('/admin/scraper-status')


# ============================================
# SEARCH
# ============================================

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    navigation = load_navigation()

    results = []
    if query:
        # Search markdown content
        for item in navigation:
            if item['slug'] in ['businesses', 'dining', 'events']:
                continue
            file_path = g.paths['content_dir'] / f"{item['slug']}.md"
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
                         navigation=navigation,
                         current_page='search')


@app.route('/map')
def interactive_map():
    navigation = load_navigation()
    return render_template('map.html',
                         title='Interactive Map',
                         navigation=navigation,
                         current_page='map')


@app.route('/about')
def about():
    content, title, toc = load_markdown_content('about')
    navigation = load_navigation()
    if content is None:
        abort(404)
    return render_template('page.html',
                         content=content,
                         title=title,
                         toc=toc,
                         navigation=navigation,
                         current_page='about')


# ============================================
# SITEMAP (per-site)
# ============================================

@app.route('/sitemap.xml')
def sitemap():
    """Generate a sitemap for the current site."""
    navigation = load_navigation()
    # Force HTTPS for production
    host = request.host_url.rstrip('/').replace('http://', 'https://')

    pages = []

    # Add main pages
    pages.append({'loc': host + '/', 'priority': '1.0'})

    # Add navigation pages
    for item in navigation:
        if item['slug'] == 'overview':
            continue
        if item['slug'] in ['businesses', 'dining', 'events', 'schools', 'arts', 'worship', 'services', 'map', 'about']:
            pages.append({'loc': f"{host}/{item['slug']}", 'priority': '0.8'})
        else:
            pages.append({'loc': f"{host}/page/{item['slug']}", 'priority': '0.7'})

    # Add business pages
    for business in load_businesses():
        pages.append({'loc': f"{host}/business/{business.get('slug')}", 'priority': '0.6'})

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += f'  <url>\n    <loc>{page["loc"]}</loc>\n    <priority>{page["priority"]}</priority>\n  </url>\n'
    xml += '</urlset>'

    return xml, 200, {'Content-Type': 'application/xml'}


@app.route('/robots.txt')
def robots():
    """Generate robots.txt for the current site."""
    host = request.host_url.rstrip('/').replace('http://', 'https://')
    content = f"""User-agent: *
Allow: /

Sitemap: {host}/sitemap.xml
"""
    return content, 200, {'Content-Type': 'text/plain'}


@app.errorhandler(404)
def page_not_found(e):
    navigation = load_navigation()
    return render_template('404.html',
                         navigation=navigation,
                         current_page=None), 404


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    # For local development, you can override the site:
    # SITE_OVERRIDE=brightwood python app_multitenant.py
    print(f"Starting multi-tenant app...")
    print(f"Default site: {DEFAULT_SITE}")
    print(f"Available sites: {list(SITE_METADATA.keys())}")
    print(f"\nTo test a specific site locally:")
    print(f"  SITE_OVERRIDE=brightwood python app_multitenant.py")
    print()
    app.run(debug=True, port=5260)
