# Phase 3: Deployment Infrastructure

> Set up hosting, CI/CD, and automated deployment pipelines.

## Overview

This phase covers:
1. **GitHub Setup** - Create repositories for each site
2. **Railway Projects** - Create hosting projects linked to GitHub
3. **Deployment Automation** - Scripts to orchestrate the entire process
4. **Environment Configuration** - API tokens and secrets

## Prerequisites

Before starting:
- [ ] Domains purchased and DNS configured (Phase 2)
- [ ] GitHub account with SSH key configured
- [ ] Railway account (connected to GitHub)
- [ ] All API tokens ready (see below)

## Required API Tokens

### Token Checklist

```bash
# .env file
RAILWAY_TOKEN=railway_token_here
CLOUDFLARE_TOKEN=cloudflare_token_here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_ANALYTICS_ACCOUNT_ID=123456789
```

### Getting Railway Token

1. Go to [Railway Dashboard](https://railway.app/account/tokens)
2. Click "Create Token"
3. Name it (e.g., "deploy-automation")
4. Copy and save the token

### Getting Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable APIs:
   - Google Analytics Admin API
   - Google Analytics Data API
   - Search Console API
4. Go to IAM & Admin → Service Accounts
5. Create service account with roles:
   - Analytics Admin
   - Search Console Site Owner
6. Create and download JSON key file

## Step 1: Create GitHub Repositories

### Repository Structure

Each site needs its own repository:

```
github.com/your-username/
├── site-1
├── site-2
├── site-3
└── ...
```

### Create Repositories

```bash
# For each site
gh repo create site-1 --public --description "Site description"
gh repo create site-2 --public --description "Site description"
# ... repeat for each site
```

### Initialize and Push

```bash
cd /path/to/site-1
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:username/site-1.git
git push -u origin main
```

## Step 2: Configure Deployment Scripts

### Directory Structure

```
shared/tools/deploy/
├── config.py               # Site definitions
├── deploy_all.py           # Master orchestration
├── railway_setup.py        # Railway automation
├── cloudflare_setup.py     # DNS configuration
├── google_analytics_setup.py
├── search_console_setup.py
├── inject_analytics.py
├── generate_seo_files.py
└── requirements.txt
```

### Configuration File

Create `config.py` with your site definitions:

```python
"""
Configuration for deployment
"""

SITES = {
    "site-1": {
        "name": "Site1Name",
        "domain": "site1.com",
        "local_path": "/path/to/site-1",
        "github_repo": "site-1",
        "description": "Description of site 1"
    },
    "site-2": {
        "name": "Site2Name",
        "domain": "site2.com",
        "local_path": "/path/to/site-2",
        "github_repo": "site-2",
        "description": "Description of site 2"
    },
    # Add all your sites...
}

# GitHub organization (None for personal repos)
GITHUB_ORG = None  # or "your-org-name"

# All domains for cross-linking
ALL_DOMAINS = {
    "site1.com": "Site 1 Name",
    "site2.com": "Site 2 Name",
    # ...
}
```

### Install Dependencies

```bash
cd shared/tools/deploy
pip install -r requirements.txt
```

Required packages:
```
requests>=2.31.0
google-analytics-admin>=0.22.0
google-api-python-client>=2.100.0
google-auth>=2.23.0
python-dotenv>=1.0.0
```

## Step 3: Create Railway Projects

### Option A: Automated Setup

```bash
cd shared/tools/deploy

# List existing projects
python railway_setup.py --token $RAILWAY_TOKEN --list

# Dry run to see what will be created
python railway_setup.py --token $RAILWAY_TOKEN --dry-run

# Create all projects
python railway_setup.py --token $RAILWAY_TOKEN
```

### Option B: Manual Setup (Per Site)

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway auto-detects Python/Flask and deploys

### Railway Project Settings

Each project should have:
- Auto-deploy from `main` branch
- Nixpacks builder
- Generated domain (e.g., `site-abc123.up.railway.app`)

### Railway Configuration File

Each site needs `railway.toml`:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn app:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## Step 4: Run Full Deployment

### Master Deployment Script

The `deploy_all.py` script orchestrates everything:

```bash
cd shared/tools/deploy

# Check all prerequisites
python deploy_all.py --check

# Show deployment plan
python deploy_all.py --plan

# Dry run (no changes)
python deploy_all.py --dry-run

# Full deployment
python deploy_all.py --deploy
```

### Deployment Steps

The script runs these steps in order:

1. **Generate SEO Files** - Create sitemaps and robots.txt
2. **Railway Projects** - Create and link to GitHub
3. **Cloudflare DNS** - Configure DNS records
4. **Google Analytics** - Create GA4 properties
5. **Inject Analytics** - Add tracking code to sites
6. **Search Console** - Add and verify sites

## Step 5: Verify Deployment

### Verification Checklist

```markdown
## Site: yourdomain.com

| Check | Status | Command/Action |
|-------|--------|----------------|
| Railway running | [ ] | Check Railway dashboard |
| DNS resolves | [ ] | `dig yourdomain.com` |
| HTTPS works | [ ] | `curl -I https://yourdomain.com` |
| App responds | [ ] | Visit in browser |
| GA tracking | [ ] | Check GA4 real-time |
| Search Console | [ ] | Check GSC dashboard |
```

### Quick Verification Commands

```bash
# Check DNS
dig yourdomain.com A +short

# Check HTTPS
curl -I https://yourdomain.com 2>&1 | head -5

# Check response time
curl -w "%{time_total}s\n" -o /dev/null -s https://yourdomain.com

# Check SSL certificate
echo | openssl s_client -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates
```

## Environment File Template

Create `.env.example` for new projects:

```bash
# Railway
RAILWAY_TOKEN=

# Cloudflare
CLOUDFLARE_TOKEN=

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
GOOGLE_ANALYTICS_ACCOUNT_ID=

# Optional: OpenAI (for domain search)
OPENAI_API_KEY=

# Optional: RapidAPI (for domain availability)
RAPIDAPI_KEY=

# Optional: Notion (for documentation)
NOTION_API_KEY=
NOTION_PARENT_PAGE_ID=
```

## Troubleshooting

### Railway Deploy Fails

```bash
# Check logs
railway logs --project your-project

# Common issues:
# - Missing requirements.txt
# - Wrong Python version
# - Missing Procfile or railway.toml
```

### DNS Not Working

```bash
# Check Cloudflare zone
python cloudflare_setup.py --token $TOKEN --list-zones

# Verify records
dig yourdomain.com CNAME +short
dig yourdomain.com A +short

# Check propagation
# Visit: https://www.whatsmydns.net/
```

### Analytics Not Tracking

1. Check measurement ID is correct in source
2. Verify script is in `<head>` section
3. Check browser console for errors
4. Test with GA Debugger extension

## Files Reference

### Deployment Scripts

| File | Purpose |
|------|---------|
| `config.py` | Site definitions, domains, paths |
| `deploy_all.py` | Master orchestration |
| `railway_setup.py` | Railway API automation |
| `cloudflare_setup.py` | DNS configuration |
| `google_analytics_setup.py` | GA4 property creation |
| `search_console_setup.py` | Search Console setup |
| `inject_analytics.py` | Code injection |
| `generate_seo_files.py` | Sitemap/robots.txt |

### Output Files

| File | Purpose |
|------|---------|
| `railway_projects.json` | Railway project/service IDs |
| `ga_measurement_ids.json` | GA4 measurement IDs per site |
| `dns_records.json` | DNS record configurations |

## Output Checklist

After completing this phase:

- [ ] All GitHub repos created and pushed
- [ ] Railway projects created and linked
- [ ] All sites deploying from main branch
- [ ] Railway URLs assigned to each site
- [ ] DNS configured and propagated
- [ ] SSL certificates active
- [ ] All sites accessible via HTTPS
- [ ] Deployment automation tested

---

**Next Step:** [04-SITE-TEMPLATE-STRUCTURE.md](./04-SITE-TEMPLATE-STRUCTURE.md)
