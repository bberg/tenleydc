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

### Phase 0: Multi-Tenant Refactor (PRIORITY)
**Status: NEXT**

- [ ] Create multi-tenant app.py with domain routing
- [ ] Add domain-to-site mapping configuration
- [ ] Update templates to use site config variables
- [ ] Add per-site GA measurement ID injection
- [ ] Add per-site sitemap generation
- [ ] Test locally with hosts file spoofing
- [ ] Deploy single app to Railway
- [ ] Configure all 16 domains on one Railway service

**Estimated time:** 2-4 hours

### Phase 1: Domain Purchase
**Status: Ready when Phase 0 complete**

- [ ] Purchase 16 domains on Cloudflare (~$146)
- [ ] Point all to Railway service
- [ ] Verify SSL working on each

**Domains:**
```
DC (10): tenleydc.com, brightwooddc.com, kaloramadc.com, cheights.com,
         hstreethub.com, swdclocal.com, anacostiahub.com, shepherdparkdc.com,
         gloverdc.com, woodleyhub.com

MD (3):  collegeparkhub.com, hyattsvillehub.com, potomacspot.com

VA (3):  fallschurchhub.com, viennalocal.com, delrayva.com
```

### Phase 2: Analytics & SEO Setup

- [ ] Create 16 GA4 properties
- [ ] Add measurement IDs to config
- [ ] Verify each domain in Search Console
- [ ] Submit sitemaps for each domain

### Phase 3: Content Development (Ongoing)

Per neighborhood:
- [ ] Overview page
- [ ] Timeline
- [ ] Key historical content (3-5 pages)
- [ ] Business directory seed data
- [ ] Events setup

**Priority order:** Start with Tenleytown (most complete), then expand

### Phase 4: Revenue Setup (Optional)

- [ ] Apply for AdSense (need decent traffic first)
- [ ] Create sponsor package/rate card
- [ ] Identify 5-10 local businesses per neighborhood to approach
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

---

## Next Action

**Build the multi-tenant Flask app** - this unlocks everything else at 1/16th the hosting cost.
