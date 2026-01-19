# Multi-Site Network Deployment Workflow

> A reusable workflow guide for Claude Code projects involving domain identification, purchase, and full-stack deployment.

## Overview

This documentation captures a complete workflow for building and deploying a network of related websites. The process is broken into distinct phases that can be adapted to any multi-site project.

**Important:** As you work through this workflow, document any project-specific processes, research methods, or unique steps you develop. This documentation should grow with your project.

## Workflow Phases

| Phase | Document | Description |
|-------|----------|-------------|
| 1 | [Domain Identification](./01-DOMAIN-IDENTIFICATION.md) | Research, brainstorm, and validate domain options |
| 2 | [Domain Purchase & DNS](./02-DOMAIN-PURCHASE-DNS.md) | Register domains and configure DNS |
| 3 | [Deployment Infrastructure](./03-DEPLOYMENT-INFRASTRUCTURE.md) | Set up hosting, CI/CD, and automation scripts |
| 4 | [Site Template & Structure](./04-SITE-TEMPLATE-STRUCTURE.md) | Standard project structure and boilerplate |
| 5 | [Analytics & Monitoring](./05-ANALYTICS-MONITORING.md) | GA4, Search Console, and uptime monitoring |
| 6 | [SEO Implementation](./06-SEO-IMPLEMENTATION.md) | Sitemaps, meta tags, structured data |

## Quick Start Checklist

### Prerequisites (Human Tasks)
- [ ] Cloudflare account with payment method
- [ ] Railway account (connected to GitHub)
- [ ] Google Cloud project with service account
- [ ] GitHub account with repos ready

### API Tokens Needed
```
CLOUDFLARE_TOKEN      # API token with DNS edit permissions
RAILWAY_TOKEN         # Railway API token
GITHUB_TOKEN          # Personal access token (repo scope)
GOOGLE_APPLICATION_CREDENTIALS  # Service account JSON path
GOOGLE_ANALYTICS_ACCOUNT_ID     # GA4 account ID
```

### Estimated Timeline
- Domain research & selection: Variable (Claude can assist)
- Domain purchase: 15 minutes (manual)
- Infrastructure setup: 1-2 hours (automated)
- Site deployment: 30 minutes per site (automated)
- Analytics & monitoring: 1 hour (automated)

## Technology Stack Reference

### Hosting & Infrastructure
| Service | Purpose | Cost |
|---------|---------|------|
| Railway | App hosting | ~$5/site/month |
| Cloudflare | DNS, SSL, CDN | Free tier sufficient |
| GitHub | Source control | Free |

### Backend Stack
- Python 3.8+
- Flask 3.0+
- Gunicorn (WSGI server)

### Frontend Stack
- Vanilla HTML/CSS/JS (or framework of choice)
- No build step required for simple sites

### Monitoring & Analytics
- Google Analytics 4
- Google Search Console
- Custom monitoring agent (optional)

## Directory Structure for New Projects

```
project-network/
├── .env                    # Root secrets (gitignored)
├── .env.example            # Template for .env
├── docs/
│   ├── workflow/           # This workflow documentation
│   ├── plans/              # Project-specific planning
│   ├── domains/            # Domain research notes
│   └── processes/          # Document unique processes here
├── shared/
│   └── tools/
│       ├── deploy/         # Deployment automation scripts
│       └── domain/         # Domain search utilities
├── site-1/                 # First site
├── site-2/                 # Second site
├── site-n/                 # Additional sites
└── site-monitor/           # Monitoring agent (optional)
```

## Claude Code Integration

### Critical: Document Your Processes

As you work on this project, **carefully document** any processes you develop:

1. **Research Methods** - How you gather information for each site
2. **Content Patterns** - Templates or structures that work well
3. **Unique Workflows** - Project-specific steps not in this generic guide
4. **Lessons Learned** - What worked, what didn't

Create files in `docs/processes/` to capture this knowledge for future reference.

### Prompting Strategy

When starting a new project with Claude Code, provide:

1. **Context**: "We're building a network of X sites for [purpose]"
2. **Reference**: "Follow the workflow in docs/workflow/"
3. **Phase**: "We're currently in Phase N: [phase name]"
4. **Documentation request**: "Document any unique processes you develop in docs/processes/"

### Example Prompts by Phase

**Phase 1 - Domain Research:**
```
We need domains for a network of [N] sites about [topic].
Each site focuses on: [site1], [site2], etc.
Research and recommend domain options following docs/workflow/01-DOMAIN-IDENTIFICATION.md
Document your research process in docs/processes/domain-research.md
```

**Phase 2 - After Domain Purchase:**
```
Domains purchased: [domain1.com], [domain2.com], etc.
Configure DNS and deployment infrastructure following docs/workflow/02-DOMAIN-PURCHASE-DNS.md
```

**Phase 3 - Site Development:**
```
Create [site-name] following the template in docs/workflow/04-SITE-TEMPLATE-STRUCTURE.md
Document any content research or unique processes in docs/processes/
```

## Files to Copy to New Projects

Essential files that should be copied and adapted:

### Deployment Scripts
```
shared/tools/deploy/
├── config.py                    # Modify for your sites
├── deploy_all.py                # Master orchestration
├── railway_setup.py             # Railway automation
├── cloudflare_setup.py          # DNS configuration
├── google_analytics_setup.py    # GA4 setup
├── search_console_setup.py      # GSC setup
├── inject_analytics.py          # Code injection
├── generate_seo_files.py        # SEO files
└── requirements.txt             # Script dependencies
```

### Domain Tools
```
shared/tools/domain/
├── domain_search.py             # API-based domain search
└── check_availability.py        # WHOIS/DNS fallback
```

### Site Template (copy and rename)
```
site-template/
├── app.py
├── railway.toml
├── requirements.txt
├── Procfile
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── css/
    ├── js/
    └── favicon.svg
```

## Success Metrics

Track these metrics to measure deployment success:

- [ ] All sites returning 200 OK
- [ ] SSL certificates active (HTTPS working)
- [ ] GA4 receiving data
- [ ] Search Console verified
- [ ] Sitemaps submitted
- [ ] Response time < 2 seconds

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| DNS not propagating | Wait 5-10 min, check with `dig domain.com` |
| Railway deploy fails | Check logs: `railway logs` |
| GA4 not tracking | Verify measurement ID in source, check browser console |
| SSL errors | Ensure Cloudflare SSL mode is "Full (strict)" |

---

**Next Step:** Proceed to [01-DOMAIN-IDENTIFICATION.md](./01-DOMAIN-IDENTIFICATION.md)
