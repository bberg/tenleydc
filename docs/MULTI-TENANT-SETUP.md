# Multi-Tenant Architecture

## Overview

One Flask app (`app_multitenant.py`) serves all 16 neighborhood sites from a single Railway service ($5/month total instead of $80/month).

## How It Works

```
Request → Domain Detection → Load Site Content → Render
         ↓
         tenleydc.com → sites/tenleytown/
         brightwooddc.com → sites/brightwood/
         cheights.com → sites/columbia-heights/
         ...
```

## Domain → Site Mapping

| Domain | Site Directory |
|--------|----------------|
| tenleydc.com | sites/tenleytown/ |
| brightwooddc.com | sites/brightwood/ |
| kaloramadc.com | sites/kalorama/ |
| collegeparkhub.com | sites/college-park/ |
| hyattsvillehub.com | sites/hyattsville/ |
| potomacspot.com | sites/potomac/ |
| fallschurchhub.com | sites/falls-church/ |
| viennalocal.com | sites/vienna/ |
| delrayva.com | sites/del-ray/ |
| cheights.com | sites/columbia-heights/ |
| hstreethub.com | sites/h-street/ |
| swdclocal.com | sites/sw-waterfront/ |
| anacostiahub.com | sites/anacostia/ |
| shepherdparkdc.com | sites/shepherd-park/ |
| gloverdc.com | sites/glover-park/ |
| woodleyhub.com | sites/woodley-park/ |

## Local Development

```bash
# Default (Tenleytown)
python app_multitenant.py

# Force a specific site
SITE_OVERRIDE=brightwood python app_multitenant.py
SITE_OVERRIDE=columbia-heights python app_multitenant.py
```

App runs on **port 5260** by default.

## Railway Deployment

1. Push to GitHub
2. Connect repo to Railway
3. Add all 16 custom domains in Railway dashboard:
   - Settings → Networking → Custom Domains
   - Add each domain (tenleydc.com, brightwooddc.com, etc.)
4. Railway auto-provisions SSL for each domain

## Adding GA Tracking

Edit `app_multitenant.py`, update `SITE_METADATA`:

```python
SITE_METADATA = {
    "tenleytown": {
        "ga_id": "G-XXXXXXXXXX",  # Add your GA4 measurement ID
        ...
    },
    ...
}
```

GA ID is automatically injected via `{{ ga_id }}` in templates.

## File Structure

```
/au-park-history/
├── app_multitenant.py      # Multi-tenant entry point
├── app.py                  # Original Tenleytown app (backup)
├── Procfile                # Railway deployment config
├── sites/
│   ├── tenleytown/
│   │   ├── content/        # Markdown files
│   │   ├── data/           # JSON data
│   │   ├── templates/      # Jinja2 templates (with branding)
│   │   └── static/         # CSS/JS/images
│   ├── brightwood/
│   │   └── ...
│   └── [14 more sites]
```

## Per-Site Customization

Each site has its own:
- `content/` - Markdown content files
- `data/` - JSON data (businesses, events, schools, etc.)
- `templates/` - Templates with site-specific branding
- `static/` - Static assets

The multi-tenant app automatically loads from the correct directory based on the incoming domain.

## Cost Savings

| Setup | Monthly | Annual |
|-------|---------|--------|
| 16 separate Railway services | $80 | $960 |
| 1 multi-tenant service | $5 | $60 |
| **Savings** | **$75** | **$900** |
