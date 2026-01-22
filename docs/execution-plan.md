# Execution Plan: 16 Neighborhood History Sites

> Updated: January 2026

---

## IMMEDIATE: tenleydc.com Launch Tasks

**Site is LIVE at https://tenleydc.com** ✅

### Pending Setup Tasks

| Task | Status | Notes |
|------|--------|-------|
| Domain purchased (tenleydc.com) | ✅ Done | Cloudflare |
| Railway deployment | ✅ Done | Multi-tenant app |
| Cloudflare DNS | ✅ Done | CNAME to Railway |
| HTTPS/SSL | ✅ Done | Via Cloudflare |
| Sitemap (/sitemap.xml) | ✅ Done | Auto-generated |
| Robots.txt | ✅ Done | Auto-generated |
| **Google Analytics 4** | ✅ Done | G-FWWPBGYKR1 |
| **Google Search Console** | ✅ Done | Verified via DNS |
| **Sitemap submitted** | ✅ Done | /sitemap.xml |

**All launch tasks complete!** 🎉

---

## Business Case Assessment

### Honest Outlook

This is a **speculative side project**, not a guaranteed business. Set expectations accordingly.

| Scenario | Probability | Outcome |
|----------|-------------|---------|
| **Flop** | 40% | <1K visits/month, $0 revenue, pure cost sink |
| **Hobby break-even** | 35% | 5-10K visits, occasional sponsor, covers hosting |
| **Modest success** | 20% | 20K+ visits, $200-500/month, small profit |
| **Actual business** | 5% | 50K+ visits, $1K+/month, worth the effort |

### Costs (Annual)

| Item | Old Plan | New Plan (Multi-tenant) |
|------|----------|-------------------------|
| Domains (16 @ $9.15) | $146 | $146 |
| Hosting | $960 (16 services) | $60 (1 service) |
| **Total** | **$1,106** | **$206** |

**Savings: $900/year**

### Time Investment

| Activity | Hours/Year | Notes |
|----------|------------|-------|
| Initial build & content | 80-120 | One-time |
| Content updates/maintenance | 50-100 | Ongoing, can batch quarterly |
| Sponsor outreach (if pursued) | 40-80 | Required for revenue |
| Event scraper maintenance | 10-20 | Occasional fixes |
| **Total ongoing** | **100-200 hrs/year** | ~2-4 hrs/week average |

### Revenue Potential

| Source | Realistic Range | Effort Required |
|--------|-----------------|-----------------|
| Display ads (AdSense) | $50-150/month | Low (passive after setup) |
| Local business sponsors | $200-800/month | High (active sales) |
| Affiliate (books, tours) | $20-50/month | Low |
| Donations | $0-50/month | Low |

**Break-even requires:** ~$17/month = 1 small sponsor OR ~200K annual pageviews for ads

### Recommendation

- **If goal is profit:** Focus on 2-3 wealthy neighborhoods (Potomac, Vienna, Kalorama), kill the rest
- **If goal is portfolio/hobby:** Keep all 16, accept $206/year as entertainment cost
- **Best ROI activities:** Sponsor outreach in affluent areas, SEO for "neighborhood + history" keywords

---

## Architecture: Multi-Tenant Single App

**Key Decision:** One Flask app serves all 16 domains from one Railway service.

```
                    ┌─────────────────────┐
tenleydc.com ──────►│                     │
brightwooddc.com ──►│   Single Flask App  │──► sites/{site}/content/
cheights.com ──────►│   on Railway ($5)   │──► sites/{site}/data/
... (16 domains)    │                     │──► Per-site GA tracking
                    └─────────────────────┘
```

### How It Works

1. All 16 domains point to one Railway service
2. App reads `request.host` to determine which site
3. Loads content/data from appropriate `sites/{neighborhood}/` directory
4. Injects correct GA measurement ID per domain
5. Generates per-domain sitemaps

### Benefits

- $60/year hosting instead of $960
- Single codebase to maintain
- One deployment updates all sites
- Shared improvements benefit all sites

---

## Implementation Roadmap

### Phase 0: Multi-Tenant Infrastructure ✅ COMPLETE
**Completed: January 21, 2026**

- [x] Create multi-tenant app.py with domain routing
- [x] Add domain-to-site mapping configuration
- [x] Update templates to use site config variables
- [x] Add per-site GA measurement ID injection
- [x] Add per-site sitemap generation
- [x] Deploy single app to Railway
- [x] GitHub repo: bberg/tenleydc

### Phase 1: First Site Launch (tenleydc.com) ✅ COMPLETE
**Completed: January 21, 2026**

- [x] Purchase tenleydc.com on Cloudflare ($9.15)
- [x] Configure Cloudflare DNS (CNAME to Railway)
- [x] Verify HTTPS/SSL working
- [x] Set up GA4 property (G-FWWPBGYKR1)
- [x] Verify in Google Search Console
- [x] Submit sitemap

**Site is LIVE:** https://tenleydc.com

### Phase 2: Expand to Additional Sites
**Status: READY WHEN YOU ARE**

To add a new site:
1. Purchase domain on Cloudflare (~$9.15)
2. Add CNAME record pointing to `t4rnhnbz.up.railway.app`
3. Add custom domain in Railway dashboard
4. Create GA4 property, add ID to site template
5. Verify in Search Console, submit sitemap

**Remaining 15 domains:**
```
DC (9):  brightwooddc.com, kaloramadc.com, cheights.com,
         hstreethub.com, swdclocal.com, anacostiahub.com,
         shepherdparkdc.com, gloverdc.com, woodleyhub.com

MD (3):  collegeparkhub.com, hyattsvillehub.com, potomacspot.com

VA (3):  fallschurchhub.com, viennalocal.com, delrayva.com
```

**Recommended priority:** High-value neighborhoods first (Kalorama, Potomac, Vienna)

### Phase 3: Content Development (Ongoing)

Tenleytown content is most complete. Other sites need:
- [ ] Overview page with local history
- [ ] Timeline of key events
- [ ] Historical content (3-5 pages)
- [ ] Business directory seed data
- [ ] Local events calendar

### Phase 4: Revenue Setup (When Traffic Justifies)

- [ ] Apply for AdSense (need ~10K monthly pageviews)
- [ ] Create sponsor package/rate card
- [ ] Identify local businesses to approach
- [ ] Set up contact forms for sponsor inquiries

---

## File Structure (Multi-Tenant)

```
/au-park-history/
├── app.py                      # Multi-tenant Flask app
├── config.py                   # Domain mappings, GA IDs
├── templates/                  # Shared templates
├── static/                     # Shared CSS/JS
├── sites/
│   ├── tenleytown/
│   │   ├── content/           # Markdown files
│   │   └── data/              # JSON data files
│   ├── brightwood/
│   │   ├── content/
│   │   └── data/
│   └── ... (16 total)
└── shared/
    └── tools/
        └── deploy/
            └── config.py      # Master site configuration
```

---

## Success Metrics

### Year 1 Goals (Realistic)

| Metric | Target | Stretch |
|--------|--------|---------|
| Total monthly pageviews | 10,000 | 25,000 |
| Sites with 500+ monthly visits | 5 | 10 |
| Monthly revenue | $0 (break-even) | $100 |
| Local sponsors | 0 | 2 |

### Signals to Expand Effort

- Any site getting 5K+ monthly visits
- Inbound sponsor inquiries
- Community engagement (comments, submissions)

### Signals to Reduce Effort

- <1K total monthly visits after 6 months
- Zero organic search traffic growth
- No community engagement

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Sites become maintenance burden | Batch updates quarterly, automate what's possible |
| No traffic after 6 months | Cut to top 3-5 performers, redirect others |
| Railway pricing changes | Can migrate to $5 VPS with nginx |
| Content goes stale | Focus on evergreen history content, automate event scraping |

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Jan 2026 | Multi-tenant architecture | Saves $900/year in hosting |
| Jan 2026 | 16 neighborhoods (not 20+) | Manageable scope |
| Jan 2026 | Mixed domain naming | Good domain > fleet consistency |
| Jan 2026 | Cloudflare for domains | $9.15/domain, integrated DNS |
| Jan 21 | Launch tenleydc.com first | Validate before buying 15 more domains |
| Jan 21 | Hard-code GA IDs in templates | Context processor had Railway caching issues |
| Jan 21 | GitHub repo: bberg/tenleydc | Railway auto-deploys on push |

---

## Current Status (January 21, 2026)

**LIVE:** https://tenleydc.com
- Multi-tenant Flask app deployed on Railway
- GA4 tracking active (G-FWWPBGYKR1)
- Google Search Console verified
- Sitemap submitted

**Costs so far:**
- Domain: $9.15/year
- Hosting: ~$5/month ($60/year)
- **Total: ~$69/year** for first site

---

## Next Steps

### Immediate (This Week)
1. **Monitor GA4** - Check analytics.google.com for first traffic data
2. **Check Search Console** - Watch for indexing progress at search.google.com/search-console

### Short-term (Next 2-4 Weeks)
3. **Assess traffic** - Is anyone finding the site organically?
4. **Content polish** - Fill gaps in Tenleytown content
5. **Decide on expansion** - Add 2-3 more sites or wait?

### If Expanding
6. **Buy high-value domains first:** kaloramadc.com, potomacspot.com, viennalocal.com
7. **Replicate setup** for each (DNS, Railway, GA4, Search Console)
8. **Build out content** for each neighborhood

### If Traffic Materializes (1K+ monthly)
9. **Apply for AdSense**
10. **Create sponsor outreach materials**
11. **Contact local businesses**
