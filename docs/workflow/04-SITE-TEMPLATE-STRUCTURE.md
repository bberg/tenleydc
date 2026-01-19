# Phase 4: Site Template & Structure

> Standard project structure and boilerplate for consistent site development.

## Overview

This phase covers:
1. **Standard Directory Structure** - Consistent layout for all sites
2. **Flask Application Template** - Backend boilerplate
3. **Frontend Structure** - HTML, CSS, JS organization
4. **SEO Infrastructure** - Sitemaps, robots.txt, meta tags
5. **Deployment Files** - Railway and Git configuration

## Standard Directory Structure

```
site-name/
├── app.py                    # Flask application entry point
├── railway.toml              # Railway deployment config
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn startup command
├── .gitignore                # Git ignore rules
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base template with shared layout
│   ├── index.html            # Homepage
│   └── [feature].html        # Additional pages
│
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   ├── js/
│   │   └── app.js            # Main JavaScript
│   ├── images/               # Image assets
│   ├── favicon.svg           # Site favicon
│   ├── robots.txt            # (Static fallback)
│   └── sitemap.xml           # (Static fallback)
│
├── research/                 # Site-specific research (optional)
│   └── [research-docs].md
│
├── plans/                    # Development roadmap (optional)
│   └── roadmap.md
│
└── docs/                     # Site-specific documentation
    └── [site-docs].md
```

## File Templates

### app.py - Flask Application

```python
from flask import Flask, render_template, send_from_directory, Response
from datetime import datetime
import os

app = Flask(__name__)

# ============================================
# Main Routes
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

# Add additional routes as needed
# @app.route('/about')
# def about():
#     return render_template('about.html', active_page='about')

# ============================================
# Static Files
# ============================================

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.svg',
        mimetype='image/svg+xml'
    )

# ============================================
# SEO Routes
# ============================================

@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap"""
    today = datetime.now().strftime('%Y-%m-%d')
    domain = "https://yourdomain.com"  # Update this

    # Define your pages
    pages = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        # Add more pages as needed
    ]

    urls = []
    for page in pages:
        urls.append(f'''    <url>
        <loc>{domain}{page['loc']}</loc>
        <lastmod>{today}</lastmod>
        <priority>{page['priority']}</priority>
        <changefreq>{page['changefreq']}</changefreq>
    </url>''')

    sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt"""
    domain = "https://yourdomain.com"  # Update this

    robots_txt = f'''User-agent: *
Allow: /
Sitemap: {domain}/sitemap.xml

Crawl-delay: 1'''

    return Response(robots_txt, mimetype='text/plain')

# ============================================
# Entry Point
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
```

### requirements.txt

```
Flask==3.0.0
gunicorn==21.2.0
```

Add additional packages as needed:
```
# For database
Flask-SQLAlchemy==3.1.1

# For forms
Flask-WTF==1.2.1

# For scheduling
APScheduler==3.10.4

# For API requests
requests==2.31.0
```

### railway.toml

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn app:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Procfile

```
web: gunicorn app:app
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project
*.log
*.tmp
node_modules/
```

## HTML Templates

### templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO Meta Tags -->
    <title>{% block title %}Site Name{% endblock %}</title>
    <meta name="description" content="{% block description %}Site description{% endblock %}">
    <meta name="keywords" content="{% block keywords %}keyword1, keyword2{% endblock %}">

    <!-- Open Graph -->
    <meta property="og:title" content="{% block og_title %}{{ self.title() }}{% endblock %}">
    <meta property="og:description" content="{% block og_description %}{{ self.description() }}{% endblock %}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{% block og_url %}https://yourdomain.com{% endblock %}">

    <!-- Favicon -->
    <link rel="icon" href="/static/favicon.svg" type="image/svg+xml">

    <!-- Styles -->
    <link rel="stylesheet" href="/static/css/style.css">
    {% block extra_css %}{% endblock %}

    <!-- Google Analytics (injected by deploy scripts) -->
    {% block analytics %}{% endblock %}
</head>
<body>
    <header>
        {% block header %}
        <nav>
            <a href="/" class="logo">Site Name</a>
            <ul>
                <li><a href="/">Home</a></li>
                <!-- Add navigation items -->
            </ul>
        </nav>
        {% endblock %}
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        {% block footer %}
        <p>&copy; {{ now().year }} Site Name. All rights reserved.</p>
        <nav>
            <!-- Network links -->
        </nav>
        {% endblock %}
    </footer>

    <!-- Scripts -->
    <script src="/static/js/app.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### templates/index.html

```html
{% extends "base.html" %}

{% block title %}Site Name - Main Feature{% endblock %}
{% block description %}Compelling description of what this site does.{% endblock %}
{% block keywords %}primary keyword, secondary keyword, feature{% endblock %}

{% block content %}
<section class="hero">
    <h1>Main Headline</h1>
    <p>Subheadline explaining the value proposition.</p>
</section>

<section class="main-content">
    <!-- Main site content -->
</section>

<section class="features">
    <h2>Features</h2>
    <!-- Feature list -->
</section>
{% endblock %}

{% block extra_js %}
<script src="/static/js/app.js"></script>
{% endblock %}
```

## Static Assets

### static/css/style.css

```css
/* ============================================
   CSS Reset & Base
   ============================================ */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    /* Color palette - customize per site */
    --color-primary: #2563eb;
    --color-secondary: #64748b;
    --color-background: #ffffff;
    --color-surface: #f8fafc;
    --color-text: #1e293b;
    --color-text-muted: #64748b;

    /* Typography */
    --font-sans: system-ui, -apple-system, sans-serif;
    --font-mono: ui-monospace, monospace;

    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 2rem;
    --spacing-xl: 4rem;

    /* Border radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 16px;
}

body {
    font-family: var(--font-sans);
    color: var(--color-text);
    background: var(--color-background);
    line-height: 1.6;
}

/* ============================================
   Layout
   ============================================ */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

/* ============================================
   Components
   ============================================ */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-primary {
    background: var(--color-primary);
    color: white;
    border: none;
}

.btn-primary:hover {
    opacity: 0.9;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 768px) {
    :root {
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
    }
}
```

### static/js/app.js

```javascript
/**
 * Main Application JavaScript
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

/**
 * Initialize the application
 */
function initApp() {
    console.log('App initialized');
    // Add your initialization code here
}

// ============================================
// Utility Functions
// ============================================

/**
 * Debounce function for performance
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
```

### static/favicon.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#2563eb"/>
  <text x="50" y="65" font-size="50" text-anchor="middle" fill="white" font-family="system-ui">S</text>
</svg>
```

## Creating a New Site

### Quick Start Checklist

1. **Copy template structure**
   ```bash
   cp -r site-template/ new-site/
   cd new-site
   ```

2. **Update configuration**
   - `app.py`: Update domain references
   - `templates/base.html`: Update site name
   - `static/css/style.css`: Customize colors

3. **Initialize Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Create GitHub repo**
   ```bash
   gh repo create new-site --public
   git remote add origin git@github.com:username/new-site.git
   git push -u origin main
   ```

5. **Add to deployment config**

   Update `shared/tools/deploy/config.py`:
   ```python
   SITES["new-site"] = {
       "name": "NewSite",
       "domain": "newsite.com",
       "local_path": "/path/to/new-site",
       "github_repo": "new-site",
       "description": "Description of new site"
   }
   ```

6. **Run deployment**
   ```bash
   cd shared/tools/deploy
   python deploy_all.py --deploy
   ```

## Local Development

### Running Locally

```bash
cd site-name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
# or
flask run --port 8000
```

### Development with Auto-reload

```bash
FLASK_DEBUG=1 flask run --port 8000
```

### Testing Production Config Locally

```bash
gunicorn app:app --bind 0.0.0.0:8000
```

## Output Checklist

For each new site, verify:

- [ ] `app.py` with all routes
- [ ] `railway.toml` configured
- [ ] `requirements.txt` with dependencies
- [ ] `Procfile` for Gunicorn
- [ ] `.gitignore` in place
- [ ] `templates/base.html` with SEO tags
- [ ] `templates/index.html` homepage
- [ ] `static/css/style.css` styled
- [ ] `static/js/app.js` initialized
- [ ] `static/favicon.svg` created
- [ ] Sitemap route working
- [ ] Robots.txt route working
- [ ] Git repo initialized
- [ ] GitHub repo created
- [ ] Added to deployment config

---

**Next Step:** [05-ANALYTICS-MONITORING.md](./05-ANALYTICS-MONITORING.md)
