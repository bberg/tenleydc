#!/usr/bin/env python3
"""
Update site branding across all 16 neighborhood sites.
Updates app.py and base.html with correct site names and domains.
"""

import os
import re
from pathlib import Path

# Site configurations with branding details
SITE_CONFIGS = {
    "tenleytown": {
        "domain": "tenleydc.com",
        "site_name": "Tenley DC",
        "tagline": "Tenleytown, AU Park & Upper Northwest DC",
        "footer_desc": "Documenting the rich history of Tenleytown and Upper Northwest DC from the 1800s to the present.",
        "region": "Northwest Washington DC"
    },
    "brightwood": {
        "domain": "brightwooddc.com",
        "site_name": "Brightwood Almanac",
        "tagline": "History and community of Brightwood, DC",
        "footer_desc": "Documenting the rich history of Brightwood from Vinegar Hill to the present day.",
        "region": "Northwest Washington DC"
    },
    "kalorama": {
        "domain": "kaloramadc.com",
        "site_name": "Kalorama Almanac",
        "tagline": "History and community of Kalorama, DC",
        "footer_desc": "Documenting the elegant history of Kalorama from the Barker estate to Embassy Row.",
        "region": "Northwest Washington DC"
    },
    "college-park": {
        "domain": "collegeparkhub.com",
        "site_name": "College Park Almanac",
        "tagline": "History and community of College Park, Maryland",
        "footer_desc": "Documenting the history of College Park from its agricultural roots to university town.",
        "region": "Prince George's County, Maryland"
    },
    "hyattsville": {
        "domain": "hyattsvillehub.com",
        "site_name": "Hyattsville Almanac",
        "tagline": "History and community of Hyattsville, Maryland",
        "footer_desc": "Documenting the history of Hyattsville from its founding to today's arts district.",
        "region": "Prince George's County, Maryland"
    },
    "potomac": {
        "domain": "potomacspot.com",
        "site_name": "Potomac Almanac",
        "tagline": "History and community of Potomac, Maryland",
        "footer_desc": "Documenting the history of Potomac from rural farmland to distinguished community.",
        "region": "Montgomery County, Maryland"
    },
    "falls-church": {
        "domain": "fallschurchhub.com",
        "site_name": "Falls Church Almanac",
        "tagline": "History and community of Falls Church, Virginia",
        "footer_desc": "Documenting the history of The Little City from colonial times to today.",
        "region": "Northern Virginia"
    },
    "vienna": {
        "domain": "viennalocal.com",
        "site_name": "Vienna Almanac",
        "tagline": "History and community of Vienna, Virginia",
        "footer_desc": "Documenting Vienna's history from Civil War crossroads to thriving town.",
        "region": "Fairfax County, Virginia"
    },
    "del-ray": {
        "domain": "delrayva.com",
        "site_name": "Del Ray Almanac",
        "tagline": "History and community of Del Ray, Alexandria",
        "footer_desc": "Documenting Del Ray's evolution from streetcar suburb to vibrant neighborhood.",
        "region": "Alexandria, Virginia"
    },
    "columbia-heights": {
        "domain": "cheights.com",
        "site_name": "Columbia Heights Almanac",
        "tagline": "History and community of Columbia Heights, DC",
        "footer_desc": "Documenting Columbia Heights from Meridian Hill to today's diverse neighborhood.",
        "region": "Northwest Washington DC"
    },
    "h-street": {
        "domain": "hstreethub.com",
        "site_name": "H Street Almanac",
        "tagline": "History and community of the H Street Corridor",
        "footer_desc": "Documenting the H Street Corridor from Great Black Broadway to today's renaissance.",
        "region": "Northeast Washington DC"
    },
    "sw-waterfront": {
        "domain": "swdclocal.com",
        "site_name": "SW Waterfront Almanac",
        "tagline": "History and community of Southwest DC",
        "footer_desc": "Documenting Southwest Waterfront from the wharf to urban renewal to The Wharf.",
        "region": "Southwest Washington DC"
    },
    "anacostia": {
        "domain": "anacostiahub.com",
        "site_name": "Anacostia Almanac",
        "tagline": "History and community of Anacostia, DC",
        "footer_desc": "Documenting Anacostia from Frederick Douglass to today's historic community.",
        "region": "Southeast Washington DC"
    },
    "shepherd-park": {
        "domain": "shepherdparkdc.com",
        "site_name": "Shepherd Park Almanac",
        "tagline": "History and community of Shepherd Park, DC",
        "footer_desc": "Documenting Shepherd Park's history as a model integrated neighborhood.",
        "region": "Northwest Washington DC"
    },
    "glover-park": {
        "domain": "gloverdc.com",
        "site_name": "Glover Park Almanac",
        "tagline": "History and community of Glover Park, DC",
        "footer_desc": "Documenting Glover Park from the Glover estate to today's neighborhood.",
        "region": "Northwest Washington DC"
    },
    "woodley-park": {
        "domain": "woodleyhub.com",
        "site_name": "Woodley Park Almanac",
        "tagline": "History and community of Woodley Park, DC",
        "footer_desc": "Documenting Woodley Park from the Woodley Mansion to today's urban village.",
        "region": "Northwest Washington DC"
    }
}

BASE_PATH = Path("/Users/bb/www/au-park-history/sites")


def update_base_html(site_dir: str, config: dict):
    """Update base.html with correct branding"""
    base_html_path = BASE_PATH / site_dir / "templates" / "base.html"

    if not base_html_path.exists():
        print(f"  WARNING: {base_html_path} not found")
        return False

    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update title tag
    content = re.sub(
        r'<title>{% if title %}{{ title }} \| {% endif %}[^<]+</title>',
        f'<title>{{% if title %}}{{{{ title }}}} | {{% endif %}}{config["site_name"]}</title>',
        content
    )

    # Update logo-main
    content = re.sub(
        r'<span class="logo-main">[^<]+</span>',
        f'<span class="logo-main">{config["site_name"]}</span>',
        content
    )

    # Update logo-sub
    content = re.sub(
        r'<span class="logo-sub">[^<]+</span>',
        f'<span class="logo-sub">{config["region"]}</span>',
        content
    )

    # Update mobile logo
    content = re.sub(
        r'<a href="/" class="mobile-logo">[^<]+</a>',
        f'<a href="/" class="mobile-logo">{config["site_name"]}</a>',
        content
    )

    # Update footer title
    content = re.sub(
        r'<span class="footer-title">[^<]+</span>',
        f'<span class="footer-title">{config["site_name"]}</span>',
        content
    )

    # Update footer tagline
    content = re.sub(
        r'<span class="footer-tagline">[^<]+</span>',
        f'<span class="footer-tagline">{config["tagline"]}</span>',
        content
    )

    # Update footer description
    content = re.sub(
        r'<p class="footer-desc">[^<]+</p>',
        f'<p class="footer-desc">{config["footer_desc"]}</p>',
        content
    )

    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def update_app_py(site_dir: str, config: dict):
    """Update app.py docstring with correct site name"""
    app_py_path = BASE_PATH / site_dir / "app.py"

    if not app_py_path.exists():
        print(f"  WARNING: {app_py_path} not found")
        return False

    with open(app_py_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update docstring at top of file
    # Match pattern: """Something Almanac\nA Flask application..."""
    content = re.sub(
        r'"""[^"]*Almanac\nA Flask application documenting the history of [^"]+"""',
        f'"""{config["site_name"]}\nA Flask application documenting the history of {config["tagline"].replace("History and community of ", "")}"""',
        content
    )

    # Add site config if not present
    if "SITE_CONFIG" not in content:
        # Find the line after app = Flask(__name__)
        insert_point = content.find("app = Flask(__name__)")
        if insert_point != -1:
            insert_point = content.find("\n", insert_point) + 1
            site_config_block = f'''
# Site configuration
SITE_CONFIG = {{
    "domain": "{config["domain"]}",
    "site_name": "{config["site_name"]}",
    "tagline": "{config["tagline"]}",
    "region": "{config["region"]}"
}}

'''
            content = content[:insert_point] + site_config_block + content[insert_point:]

    with open(app_py_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    """Update all sites with correct branding"""
    print("Updating site branding for 16 neighborhood sites...\n")

    for site_dir, config in SITE_CONFIGS.items():
        print(f"Updating {site_dir} -> {config['domain']}")

        # Update base.html
        if update_base_html(site_dir, config):
            print(f"  - Updated templates/base.html")

        # Update app.py
        if update_app_py(site_dir, config):
            print(f"  - Updated app.py")

        print()

    print("Done! All 16 sites updated.")


if __name__ == "__main__":
    main()
