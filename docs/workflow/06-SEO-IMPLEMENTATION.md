# Phase 6: SEO Implementation

> Implement sitemaps, meta tags, structured data, and content optimization for search visibility.

## Overview

This phase covers:
1. **Technical SEO** - Sitemaps, robots.txt, canonical URLs
2. **On-Page SEO** - Meta tags, headings, content structure
3. **Structured Data** - JSON-LD schema markup
4. **Content Strategy** - Page optimization and expansion

## Part 1: Technical SEO

### Sitemap Implementation

#### Dynamic Sitemap Route

```python
# app.py
from flask import Response
from datetime import datetime

@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic XML sitemap."""
    domain = "https://yourdomain.com"
    today = datetime.now().strftime('%Y-%m-%d')

    # Define all pages
    pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'url': '/about', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/features', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/faq', 'priority': '0.7', 'changefreq': 'monthly'},
    ]

    # Add dynamic pages if needed
    # for item in get_dynamic_pages():
    #     pages.append({'url': item.url, 'priority': '0.6', 'changefreq': 'weekly'})

    urls = []
    for page in pages:
        urls.append(f'''    <url>
        <loc>{domain}{page['url']}</loc>
        <lastmod>{today}</lastmod>
        <priority>{page['priority']}</priority>
        <changefreq>{page['changefreq']}</changefreq>
    </url>''')

    sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

    return Response(sitemap_xml, mimetype='application/xml')
```

#### Priority Guidelines

| Page Type | Priority | Change Frequency |
|-----------|----------|------------------|
| Homepage | 1.0 | weekly |
| Main feature pages | 0.9 | weekly |
| Secondary pages | 0.8 | monthly |
| About/Contact | 0.7 | monthly |
| Blog posts | 0.6 | yearly |
| Legal pages | 0.3 | yearly |

### Robots.txt Implementation

```python
@app.route('/robots.txt')
def robots():
    """Serve robots.txt for search engines."""
    domain = "https://yourdomain.com"

    robots_txt = f'''User-agent: *
Allow: /

# Sitemap location
Sitemap: {domain}/sitemap.xml

# Crawl delay (be polite to servers)
Crawl-delay: 1

# Block admin/internal paths (if any)
# Disallow: /admin/
# Disallow: /api/
'''

    return Response(robots_txt, mimetype='text/plain')
```

### Canonical URLs

Add to every page to prevent duplicate content:

```html
<link rel="canonical" href="https://yourdomain.com{{ request.path }}">
```

Or in Flask:
```python
@app.context_processor
def inject_canonical():
    return {
        'canonical_url': f"https://yourdomain.com{request.path}"
    }
```

## Part 2: On-Page SEO

### Meta Tags Template

```html
<head>
    <!-- Primary Meta Tags -->
    <title>{{ title }} | Site Name</title>
    <meta name="title" content="{{ title }} | Site Name">
    <meta name="description" content="{{ description }}">
    <meta name="keywords" content="{{ keywords }}">
    <meta name="author" content="Your Name">

    <!-- Canonical -->
    <link rel="canonical" href="{{ canonical_url }}">

    <!-- Robots -->
    <meta name="robots" content="index, follow">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ canonical_url }}">
    <meta property="og:title" content="{{ title }}">
    <meta property="og:description" content="{{ description }}">
    <meta property="og:image" content="{{ og_image }}">
    <meta property="og:site_name" content="Site Name">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{{ canonical_url }}">
    <meta name="twitter:title" content="{{ title }}">
    <meta name="twitter:description" content="{{ description }}">
    <meta name="twitter:image" content="{{ og_image }}">

    <!-- Mobile -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#2563eb">
</head>
```

### Centralized SEO Metadata

Create a metadata file for all pages:

```python
# seo_data.py
"""Centralized SEO metadata for all pages."""

SITE_NAME = "Your Site Name"
DEFAULT_IMAGE = "/static/og-images/default.png"

PAGE_METADATA = {
    'index': {
        'title': 'Main Feature - Free Online Resource',
        'description': 'A compelling 150-160 character description that includes your primary keyword.',
        'keywords': 'primary keyword, secondary keyword, feature',
        'og_image': '/static/og-images/home.png',
    },
    'about': {
        'title': 'About Us',
        'description': 'Learn about our mission and what we do.',
        'keywords': 'about, company, mission',
        'og_image': DEFAULT_IMAGE,
    },
    # Add more pages...
}

def get_page_meta(page_name, **kwargs):
    """Get metadata for a page, with optional template variables."""
    meta = PAGE_METADATA.get(page_name, PAGE_METADATA['index']).copy()

    # Handle templates with variables
    for key in ['title', 'description', 'keywords']:
        if '{' in meta.get(key, ''):
            meta[key] = meta[key].format(**kwargs)

    meta.setdefault('og_image', DEFAULT_IMAGE)
    return meta
```

Usage in Flask:
```python
from seo_data import get_page_meta, SITE_NAME

@app.route('/')
def index():
    meta = get_page_meta('index')
    return render_template('index.html', meta=meta, site_name=SITE_NAME)
```

### Heading Structure

Follow semantic heading hierarchy:

```html
<body>
    <header>
        <h1>Main Page Title (Only One H1)</h1>
    </header>

    <main>
        <section>
            <h2>Primary Section Heading</h2>
            <p>Content...</p>

            <h3>Subsection Heading</h3>
            <p>More content...</p>
        </section>

        <section>
            <h2>Another Section</h2>
            <h3>Subsection A</h3>
            <h3>Subsection B</h3>
        </section>
    </main>
</body>
```

## Part 3: Structured Data (JSON-LD)

### WebSite Schema

For your main site:

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Site Name",
    "description": "Site description",
    "url": "https://yourdomain.com"
}
</script>
```

### Organization Schema

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Your Organization",
    "url": "https://yourdomain.com",
    "logo": "https://yourdomain.com/static/logo.png"
}
</script>
```

### FAQPage Schema

For FAQ sections (helps get rich snippets):

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "What is this site about?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "This site provides..."
            }
        },
        {
            "@type": "Question",
            "name": "Is it free to use?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes, this service is completely free..."
            }
        }
    ]
}
</script>
```

### BreadcrumbList Schema

For navigation breadcrumbs:

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://yourdomain.com/"
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Category",
            "item": "https://yourdomain.com/category"
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Current Page",
            "item": "https://yourdomain.com/category/page"
        }
    ]
}
</script>
```

### Dynamic Schema Generation

```python
# schema.py
import json

def generate_website_schema(name, description, url):
    """Generate WebSite JSON-LD schema."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": name,
        "description": description,
        "url": url
    }, indent=2)

def generate_faq_schema(questions):
    """Generate FAQPage JSON-LD schema.

    Args:
        questions: List of dicts with 'question' and 'answer' keys
    """
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": q["answer"]
                }
            }
            for q in questions
        ]
    }, indent=2)
```

## Part 4: Content Optimization

### Content Guidelines

1. **Minimum Word Count**
   - Homepage: 500+ words
   - Feature pages: 800+ words
   - Blog posts: 1500+ words

2. **Keyword Placement**
   - Title tag (beginning preferred)
   - H1 heading
   - First paragraph
   - Subheadings (H2, H3)
   - Image alt text
   - URL slug

3. **Content Structure**
   - Clear introduction
   - Scannable sections
   - Bullet points and lists
   - Internal links
   - Call-to-action

### Image Optimization

```html
<!-- Always include alt text -->
<img src="/static/images/feature.png"
     alt="Descriptive alt text explaining the image content"
     width="800"
     height="600"
     loading="lazy">
```

Best practices:
- Descriptive alt text (not just "image")
- Include width and height attributes
- Use lazy loading for below-fold images
- Compress images (WebP format preferred)
- Use descriptive filenames

### Internal Linking Strategy

Link between related pages in your network:

```html
<p>
    Related resources you might find helpful:
    <a href="https://site2.com">Related Site 2</a> and
    <a href="https://site3.com">Related Site 3</a>.
</p>
```

Add network footer for cross-linking:

```html
<footer>
    <nav aria-label="Network Sites">
        <h3>Our Network</h3>
        <ul>
            <li><a href="https://site1.com">Site 1</a></li>
            <li><a href="https://site2.com">Site 2</a></li>
            <li><a href="https://site3.com">Site 3</a></li>
        </ul>
    </nav>
</footer>
```

## Part 5: Automated SEO File Generation

### SEO Generation Script

```python
# generate_seo_files.py
"""Generate sitemap.xml and robots.txt for all sites."""

import os
from datetime import datetime
from config import SITES

def generate_sitemap(domain, pages):
    """Generate sitemap XML content."""
    today = datetime.now().strftime('%Y-%m-%d')

    urls = []
    for page in pages:
        urls.append(f'''    <url>
        <loc>https://{domain}{page['url']}</loc>
        <lastmod>{today}</lastmod>
        <priority>{page['priority']}</priority>
        <changefreq>{page['changefreq']}</changefreq>
    </url>''')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

def generate_robots(domain):
    """Generate robots.txt content."""
    return f'''User-agent: *
Allow: /
Sitemap: https://{domain}/sitemap.xml
Crawl-delay: 1
'''

def generate_all_sites(dry_run=False):
    """Generate SEO files for all configured sites."""
    results = {}

    for site_key, site_config in SITES.items():
        domain = site_config['domain']
        local_path = site_config['local_path']
        static_dir = os.path.join(local_path, 'static')

        # Default pages (customize per site)
        pages = [
            {'url': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        ]

        print(f"\nGenerating SEO files for: {domain}")

        if dry_run:
            print(f"  [DRY RUN] Would generate sitemap.xml")
            print(f"  [DRY RUN] Would generate robots.txt")
            results[site_key] = {'status': 'dry_run'}
            continue

        # Generate files
        sitemap_content = generate_sitemap(domain, pages)
        robots_content = generate_robots(domain)

        # Write to static directory
        os.makedirs(static_dir, exist_ok=True)

        with open(os.path.join(static_dir, 'sitemap.xml'), 'w') as f:
            f.write(sitemap_content)

        with open(os.path.join(static_dir, 'robots.txt'), 'w') as f:
            f.write(robots_content)

        print(f"  Created: static/sitemap.xml")
        print(f"  Created: static/robots.txt")
        results[site_key] = {'status': 'success'}

    return results
```

## Verification Checklist

### Technical SEO

- [ ] Sitemap.xml accessible at /sitemap.xml
- [ ] Sitemap submitted to Search Console
- [ ] Robots.txt accessible at /robots.txt
- [ ] Canonical URLs on all pages
- [ ] No noindex tags on important pages
- [ ] HTTPS enabled (no mixed content)

### On-Page SEO

- [ ] Unique title tags (50-60 characters)
- [ ] Unique meta descriptions (150-160 characters)
- [ ] One H1 per page
- [ ] Logical heading hierarchy
- [ ] Keywords in key locations
- [ ] Alt text on all images

### Structured Data

- [ ] Valid JSON-LD on key pages
- [ ] Test with [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] No errors in Search Console
- [ ] FAQPage schema on FAQ sections

### Content

- [ ] 500+ words on homepage
- [ ] Internal links to related pages
- [ ] Network footer with cross-links
- [ ] Mobile-friendly layout
- [ ] Fast loading (< 3 seconds)

## Tools for Testing

1. **Google Search Console** - Index status, search performance
2. **[Rich Results Test](https://search.google.com/test/rich-results)** - Schema validation
3. **[PageSpeed Insights](https://pagespeed.web.dev/)** - Performance metrics
4. **[Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)** - Mobile usability
5. **[Screaming Frog](https://www.screamingfrog.co.uk/)** - Site audit

## Files Reference

| File | Purpose |
|------|---------|
| `seo_data.py` | Centralized metadata |
| `schema.py` | JSON-LD generators |
| `generate_seo_files.py` | Static file generation |
| `templates/base.html` | Meta tag template |

---

## Workflow Complete

You've completed the full workflow documentation. Here's a quick recap:

1. **[Phase 1](./01-DOMAIN-IDENTIFICATION.md)** - Research and select domains
2. **[Phase 2](./02-DOMAIN-PURCHASE-DNS.md)** - Purchase domains, configure DNS
3. **[Phase 3](./03-DEPLOYMENT-INFRASTRUCTURE.md)** - Set up hosting and CI/CD
4. **[Phase 4](./04-SITE-TEMPLATE-STRUCTURE.md)** - Create sites from template
5. **[Phase 5](./05-ANALYTICS-MONITORING.md)** - Add analytics and monitoring
6. **[Phase 6](./06-SEO-IMPLEMENTATION.md)** - Implement SEO (this document)

Return to [Workflow Overview](./00-WORKFLOW-OVERVIEW.md) for quick reference.

---

## Process Documentation Reminder

As you complete this workflow, document any unique processes in `docs/processes/`:
- Content research methods
- Data gathering techniques
- Site-specific workflows
- Lessons learned

This documentation will be invaluable for future projects and team members.
