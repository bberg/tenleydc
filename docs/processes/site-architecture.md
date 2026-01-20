# Site Architecture Guide

> Technical structure of each neighborhood site and how to replicate it.

---

## Technology Stack

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0+** - Web framework
- **Gunicorn** - WSGI server (production)
- **Markdown** - Content format with extensions

### Frontend
- **Vanilla HTML/CSS/JS** - No build step required
- **Font Awesome** - Icons
- **Google Fonts** - Typography (Playfair Display, Source Serif 4, Source Sans 3)

### Deployment
- **Railway** - Hosting (~$5/site/month)
- **Cloudflare** - DNS and CDN (free tier)
- **GitHub** - Source control

---

## Directory Structure

```
neighborhood-site/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── railway.toml             # Railway configuration
├── Procfile                 # Process definition
│
├── content/                 # Markdown content files
│   ├── about.md
│   ├── overview.md
│   ├── timeline.md
│   ├── [topic].md
│   └── resources.md
│
├── data/                    # JSON data files
│   ├── businesses.json
│   ├── categories.json
│   ├── events.json
│   ├── schools.json
│   ├── arts.json
│   ├── religious.json
│   ├── services.json
│   └── sources.json
│
├── templates/               # Jinja2 templates
│   ├── base.html           # Shared layout
│   ├── home.html           # Homepage
│   ├── page.html           # Content pages
│   ├── search.html         # Search results
│   ├── map.html            # Interactive map
│   ├── 404.html            # Error page
│   ├── business-directory.html
│   ├── business-profile.html
│   ├── dining.html
│   ├── schools.html
│   ├── school-profile.html
│   ├── arts.html
│   ├── arts-profile.html
│   ├── worship.html
│   ├── worship-profile.html
│   ├── services.html
│   ├── services-profile.html
│   ├── events.html
│   └── admin/
│       ├── review_events.html
│       └── scraper_status.html
│
├── static/
│   ├── css/
│   │   └── style.css       # All styles
│   ├── js/
│   │   └── main.js         # All JavaScript
│   └── images/             # Photos, maps, logos
│
└── scraper/                 # Event scraping (optional)
    ├── __init__.py
    ├── config.py
    ├── base_scraper.py
    ├── utils/
    └── scrapers/
```

---

## Flask Application (app.py)

### Core Configuration

```python
from flask import Flask, render_template, request
from pathlib import Path
import json
import markdown

app = Flask(__name__)

CONTENT_DIR = Path('content')
DATA_DIR = Path('data')

# Markdown extensions
MD_EXTENSIONS = ['tables', 'fenced_code', 'toc', 'attr_list', 'def_list', 'footnotes']
```

### Navigation Structure

Navigation is defined as a list of dictionaries with 5 groups:

```python
NAVIGATION = [
    # Main (no group - always visible)
    {'slug': 'overview', 'title': 'Overview', 'icon': 'home', 'group': None},
    {'slug': 'events', 'title': 'Events', 'icon': 'calendar', 'group': None},
    {'slug': 'map', 'title': 'Interactive Map', 'icon': 'map-marker-alt', 'group': None},

    # Community
    {'slug': 'schools', 'title': 'Schools', 'icon': 'school', 'group': 'Community'},
    {'slug': 'arts', 'title': 'Arts & Culture', 'icon': 'palette', 'group': 'Community'},
    {'slug': 'worship', 'title': 'Houses of Worship', 'icon': 'church', 'group': 'Community'},
    {'slug': 'services', 'title': 'Public Services', 'icon': 'building', 'group': 'Community'},
    {'slug': 'businesses', 'title': 'Local Businesses', 'icon': 'store', 'group': 'Community'},
    {'slug': 'dining', 'title': 'Dining Guide', 'icon': 'utensils', 'group': 'Community'},
    {'slug': 'neighborhood_guide', 'title': 'Neighborhood Guide', 'icon': 'map-signs', 'group': 'Community'},

    # Places
    {'slug': 'tenleytown', 'title': 'Tenleytown', 'icon': 'landmark', 'group': 'Places'},
    # ... more places

    # History
    {'slug': 'timeline', 'title': 'Timeline', 'icon': 'clock', 'group': 'History'},
    # ... more history pages

    # Reference
    {'slug': 'demographics', 'title': 'Demographics', 'icon': 'chart-bar', 'group': 'Reference'},
    {'slug': 'resources', 'title': 'Resources', 'icon': 'book', 'group': 'Reference'},
    {'slug': 'about', 'title': 'About', 'icon': 'info-circle', 'group': 'Reference'},
]
```

### Route Patterns

**Content pages:**
```python
@app.route('/')
def home():
    content, title = load_markdown_content('overview')
    return render_template('home.html',
                          content=content,
                          title=title,
                          navigation=NAVIGATION,
                          current_page='overview',
                          featured_events=get_featured_events(),
                          featured_businesses=get_featured_businesses())

@app.route('/page/<slug>')
def page(slug):
    content, title = load_markdown_content(slug)
    return render_template('page.html',
                          content=content,
                          title=title,
                          navigation=NAVIGATION,
                          current_page=slug)
```

**Directory pages with filtering:**
```python
@app.route('/businesses')
def business_directory():
    businesses = load_businesses()
    categories = load_categories()

    # Filter by query params
    category = request.args.get('category')
    neighborhood = request.args.get('neighborhood')

    if category:
        businesses = [b for b in businesses if b.get('category') == category]
    if neighborhood:
        businesses = [b for b in businesses if b.get('neighborhood') == neighborhood]

    # Sort: featured first, then alphabetically
    businesses.sort(key=lambda x: (not x.get('featured', False), x.get('name', '')))

    return render_template('business-directory.html',
                          businesses=businesses,
                          categories=categories,
                          current_category=category,
                          current_neighborhood=neighborhood,
                          navigation=NAVIGATION,
                          current_page='businesses')
```

**Profile pages:**
```python
@app.route('/business/<slug>')
def business_profile(slug):
    business = get_business_by_slug(slug)
    if not business:
        abort(404)

    related = get_businesses_by_category(business.get('category'))
    related = [b for b in related if b.get('slug') != slug][:3]

    return render_template('business-profile.html',
                          business=business,
                          related_businesses=related,
                          navigation=NAVIGATION,
                          current_page='businesses')
```

### Data Loading Functions

```python
def load_businesses():
    file_path = DATA_DIR / 'businesses.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('businesses', [])

def get_business_by_slug(slug):
    businesses = load_businesses()
    for business in businesses:
        if business.get('slug') == slug:
            return business
    return None

def get_featured_businesses(limit=4):
    businesses = load_businesses()
    from datetime import date
    today = date.today().isoformat()
    featured = [b for b in businesses
                if b.get('featured') and
                b.get('featured_until', '9999-12-31') >= today]
    return featured[:limit]
```

### Content Loading

```python
def load_markdown_content(slug):
    file_path = CONTENT_DIR / f'{slug}.md'
    if not file_path.exists():
        return None, None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from first H1
    title = None
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break

    html = markdown.markdown(content, extensions=MD_EXTENSIONS)
    return html, title
```

---

## Template Structure

### base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if title %}{{ title }} | {% endif %}Site Name</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
</head>
<body>
    <div class="layout">
        <!-- Sidebar Navigation -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <a href="/" class="logo">...</a>
                <form action="/search" method="get" class="search-form">...</form>
            </div>
            <nav class="sidebar-nav">
                <!-- Grouped navigation items -->
                {% for item in navigation %}
                    <!-- Group headers with collapsible sections -->
                {% endfor %}
            </nav>
        </aside>

        <!-- Mobile Header -->
        <header class="mobile-header">...</header>

        <!-- Main Content -->
        <main class="main-content">
            <div class="content-wrapper">
                {% block content %}{% endblock %}
            </div>
            <footer class="page-footer">...</footer>
        </main>
    </div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### Dynamic URL Generation

In base.html, map slugs to routes:

```jinja2
<a href="{% if item.slug == 'overview' %}/
         {% elif item.slug == 'businesses' %}/businesses
         {% elif item.slug == 'dining' %}/dining
         {% elif item.slug == 'events' %}/events
         {% elif item.slug == 'map' %}/map
         {% elif item.slug == 'schools' %}/schools
         {% elif item.slug == 'arts' %}/arts
         {% elif item.slug == 'worship' %}/worship
         {% elif item.slug == 'services' %}/services
         {% elif item.slug == 'about' %}/about
         {% else %}/page/{{ item.slug }}
         {% endif %}">
```

---

## Data Schemas

### businesses.json

```json
{
  "businesses": [
    {
      "id": "unique-id",
      "name": "Business Name",
      "slug": "url-slug",
      "category": "dining|shopping|services|entertainment|education",
      "subcategory": "restaurant|cafe|bar|bakery|...",
      "address": "street address",
      "neighborhood": "tenleytown|van-ness|chevy-chase|...",
      "phone": "(202) xxx-xxxx",
      "website": "https://...",
      "hours": {
        "monday": "9:00 AM - 5:00 PM",
        "tuesday": "...",
        "...": "..."
      },
      "featured": true,
      "featured_until": "2026-06-01",
      "history": {
        "opened": 1984,
        "founded_by": "Name",
        "story": "Narrative text",
        "what_was_here_before": "Text",
        "neighborhood_context": "Text"
      },
      "description": "Short description",
      "tags": ["tag1", "tag2"],
      "last_updated": "2026-01-18"
    }
  ]
}
```

### events.json

```json
{
  "events": [
    {
      "id": "unique-id",
      "title": "Event Title",
      "date": "2026-01-02",
      "end_date": "2026-01-05",
      "time": "7:00pm",
      "location": "Venue Name",
      "address": "street address",
      "category": "literary|cultural|community|...",
      "description": "Event description",
      "link": "https://...",
      "free": true,
      "source": "politics-prose"
    }
  ]
}
```

### schools.json, arts.json, religious.json, services.json

Similar structure with type-specific fields.

---

## CSS Organization (style.css)

### Design Tokens

```css
:root {
    /* Paper colors */
    --paper: #faf8f3;
    --paper-dark: #f5f0e6;
    --paper-darker: #eee8db;

    /* Ink colors */
    --ink: #1a1a1a;
    --ink-light: #3d3d3d;
    --ink-lighter: #666;

    /* Accent colors */
    --accent: #8b2332;
    --accent-sepia: #8b7355;

    /* Typography */
    --font-headline: 'Playfair Display', serif;
    --font-body: 'Source Serif 4', serif;
    --font-ui: 'Source Sans 3', sans-serif;

    /* Layout */
    --sidebar-width: 260px;
    --content-max-width: 1100px;
}
```

### Key Layout Patterns

```css
/* Fixed sidebar + fluid content */
.layout {
    display: grid;
    grid-template-columns: var(--sidebar-width) 1fr;
    min-height: 100vh;
}

/* Responsive: hide sidebar on mobile */
@media (max-width: 768px) {
    .sidebar { display: none; }
    .mobile-header { display: flex; }
}
```

---

## JavaScript Features (main.js)

### Key Functions

1. **Sidebar Toggle** - Mobile menu open/close
2. **Nav Groups** - Collapsible sections with localStorage persistence
3. **Search Highlighting** - Mark matched query terms
4. **Lazy Loading** - Images load on intersection
5. **Back to Top** - Floating button after scroll
6. **External Links** - Auto-target="_blank"
7. **Keyboard Navigation** - `/` focus search, `h` go home

### Nav Group Persistence

```javascript
function initNavGroups() {
    const STORAGE_KEY = 'site-nav-collapsed';
    const DEFAULT_EXPANDED = ['Community'];

    // Load saved state or use defaults
    let collapsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');

    // Apply state to nav groups
    document.querySelectorAll('.nav-group').forEach(group => {
        const groupName = group.querySelector('.nav-group-header').textContent.trim();
        if (collapsed.includes(groupName) && !DEFAULT_EXPANDED.includes(groupName)) {
            group.classList.add('collapsed');
        }
    });

    // Save state on toggle
    // ...
}
```

---

## Replication Checklist

### 1. Create Directory Structure

```bash
mkdir -p new-neighborhood-site/{content,data,templates,static/{css,js,images},scraper}
```

### 2. Copy Template Files

- Copy `app.py` and update NAVIGATION
- Copy `templates/` directory
- Copy `static/css/style.css` and `static/js/main.js`
- Copy `requirements.txt`, `railway.toml`, `Procfile`

### 3. Customize Navigation

In `app.py`, update NAVIGATION list with:
- Neighborhood-specific pages
- Relevant optional sections
- Correct icons and groupings

### 4. Update Branding

In `templates/base.html`:
- Change site name
- Update logo
- Modify footer links

In `static/css/style.css`:
- Adjust accent colors if desired
- Keep core layout consistent

### 5. Create Content Files

In `content/`:
- Create required markdown files
- Follow content structure guide
- Include proper image references

### 6. Populate Data Files

In `data/`:
- Create JSON files for each directory type
- Follow schema patterns
- Set featured content

### 7. Add Images

In `static/images/`:
- Add archival photos
- Add maps and logos
- Use descriptive filenames

### 8. Test Locally

```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

### 9. Deploy

Follow workflow documentation in `docs/workflow/`:
1. Create GitHub repository
2. Create Railway project
3. Configure Cloudflare DNS
4. Set up GA4 analytics
5. Verify in Search Console
