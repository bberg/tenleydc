# Site Replication Checklist

> Step-by-step process to create a new neighborhood site from the AU Park template.

---

## Prerequisites

Before starting:
- [ ] Market research completed (`research/[neighborhood]/market-research.md`)
- [ ] Historical research completed (`research/[neighborhood]/historical-research.md`)
- [ ] Domain identified and available
- [ ] Content outline approved

---

## Phase 1: Research (1-2 weeks)

### Market Research
- [ ] Search for existing neighborhood websites/blogs
- [ ] Identify historical societies and civic organizations
- [ ] Document competitors with strengths/weaknesses
- [ ] Find content gaps and opportunities
- [ ] Choose positioning and differentiation
- [ ] Select domain name
- [ ] Save to `research/[neighborhood]/market-research.md`

### Historical Research
- [ ] Complete Library of Congress search
- [ ] Search Chronicling America (document article counts)
- [ ] Check DC History Center catalog
- [ ] Review Internet Archive
- [ ] Download landmark nominations
- [ ] Conduct newspaper deep dive
- [ ] Gather census data
- [ ] Contact historical society
- [ ] Document sources
- [ ] Save to `research/[neighborhood]/historical-research.md`

---

## Phase 2: Content Planning (2-3 days)

### Determine Site Sections
Based on research, decide which sections to include:

**Required (every site):**
- [ ] Overview/Introduction
- [ ] Timeline
- [ ] About
- [ ] Resources

**Include if content exists:**
- [ ] Native American/Prehistory
- [ ] Neighborhood deep dive(s)
- [ ] Military history
- [ ] Transportation history
- [ ] School history
- [ ] Broadcasting/media history
- [ ] Notable institutions
- [ ] Demographics

**Community directories:**
- [ ] Local businesses
- [ ] Dining guide
- [ ] Schools
- [ ] Arts & culture
- [ ] Houses of worship
- [ ] Public services
- [ ] Events

### Create Site Plan
Document decisions in `research/[neighborhood]/site-plan.md`:
- Sections to include (with rationale)
- Navigation structure
- Style variations (if any)
- Content priorities

---

## Phase 3: Site Setup (1 day)

### Create Directory Structure
```bash
mkdir -p sites/[neighborhood]/{content,data,templates,static/{css,js,images},scraper}
```

### Copy Template Files
From `site-template/` or existing site:
- [ ] `app.py`
- [ ] `requirements.txt`
- [ ] `railway.toml`
- [ ] `Procfile`
- [ ] `templates/` directory
- [ ] `static/css/style.css`
- [ ] `static/js/main.js`

### Customize app.py
- [ ] Update NAVIGATION array for this site's sections
- [ ] Update site name in configuration
- [ ] Verify routes match planned sections
- [ ] Remove unused routes

### Customize Templates
In `templates/base.html`:
- [ ] Update site name/logo
- [ ] Update footer content
- [ ] Adjust navigation URL mappings

In `templates/home.html`:
- [ ] Update hero section
- [ ] Customize featured content areas

### Customize Styles (Optional)
In `static/css/style.css`:
- [ ] Adjust accent colors if desired
- [ ] Keep core layout consistent

---

## Phase 4: Content Creation (1-2 weeks)

### Create Markdown Content
For each section in site plan:

**Overview:**
- [ ] Create `content/overview.md`
- [ ] Include introduction to neighborhood
- [ ] Add key themes and navigation

**Timeline:**
- [ ] Create `content/timeline.md`
- [ ] Include chronological events with dates
- [ ] Cover all major eras

**Neighborhood Deep Dives:**
- [ ] Create `content/[neighborhood].md` for each
- [ ] Follow content structure template
- [ ] Include all essential elements
- [ ] Address difficult history

**Thematic Pages:**
- [ ] Create `content/[topic].md` for each
- [ ] Include specific details and sources
- [ ] Add relevant images

**Required Pages:**
- [ ] Create `content/about.md`
- [ ] Create `content/resources.md`

### Quality Check Content
For each content file:
- [ ] Verify all essential elements present
- [ ] Check for specific dates, addresses, names
- [ ] Confirm difficult history addressed
- [ ] Verify all sources attributed
- [ ] Check cross-references work
- [ ] Run through quality checklist

---

## Phase 5: Data Population (3-5 days)

### Create JSON Data Files

**businesses.json:**
- [ ] Research local businesses
- [ ] Create entries with all required fields
- [ ] Add history where known
- [ ] Set featured businesses

**categories.json:**
- [ ] Define business categories
- [ ] Create subcategories

**schools.json:**
- [ ] Research schools in area
- [ ] Include public and private
- [ ] Add history and awards

**events.json:**
- [ ] Add known recurring events
- [ ] Configure event sources for scraper

**arts.json:**
- [ ] Research arts/cultural institutions
- [ ] Include galleries, theaters, music venues

**religious.json:**
- [ ] Research houses of worship
- [ ] Include all denominations

**services.json:**
- [ ] Add libraries, recreation centers
- [ ] Include post offices, government services

**sources.json (if using scraper):**
- [ ] Configure event sources
- [ ] Set up scraper schedule

### Validate Data
- [ ] All IDs unique
- [ ] All slugs URL-safe
- [ ] All URLs valid
- [ ] Phone numbers formatted consistently
- [ ] Required fields present

---

## Phase 6: Visual Assets (2-3 days)

### Gather Images
- [ ] Download archival photos from LOC
- [ ] Request images from DC History Center
- [ ] Create AI-generated images (with disclosure)
- [ ] Optimize all images (< 500KB)

### Organize Images
```
static/images/
├── historical/          # Archival photos
├── contemporary/        # Current photos
├── maps/               # Historical and current maps
├── generated/          # AI-generated (clearly labeled)
└── logos/              # Site logos and icons
```

### Add Image Attribution
- [ ] Document source for every image
- [ ] Add alt text for accessibility
- [ ] Create caption text

---

## Phase 7: Testing (1 day)

### Local Testing
```bash
cd sites/[neighborhood]
pip install -r requirements.txt
python app.py
```

### Functionality Tests
- [ ] All navigation links work
- [ ] All content pages render
- [ ] All directory pages load
- [ ] All profile pages load
- [ ] Search returns results
- [ ] Map displays correctly
- [ ] Mobile layout correct
- [ ] Images load

### Content Verification
- [ ] Read each page thoroughly
- [ ] Check all external links
- [ ] Verify all facts against sources
- [ ] Test all interactive elements

---

## Phase 8: Deployment (1 day)

### Domain Setup
- [ ] Purchase domain (if not done)
- [ ] Configure Cloudflare DNS
- [ ] Set up SSL certificate

### Railway Deployment
- [ ] Create GitHub repository
- [ ] Create Railway project
- [ ] Connect to GitHub
- [ ] Configure environment variables
- [ ] Deploy and verify

### Analytics Setup
- [ ] Create GA4 property
- [ ] Add tracking code to site
- [ ] Configure Search Console
- [ ] Submit sitemap

---

## Phase 9: Launch Verification (1 day)

### Technical Verification
- [ ] Site accessible at domain
- [ ] HTTPS working
- [ ] All pages loading
- [ ] No console errors
- [ ] Analytics receiving data

### SEO Verification
- [ ] Robots.txt accessible
- [ ] Sitemap.xml valid
- [ ] Search Console verified
- [ ] Meta descriptions present

### Performance Check
- [ ] Page load < 3 seconds
- [ ] Mobile performance acceptable
- [ ] Images loading properly

---

## Phase 10: Post-Launch (Ongoing)

### First Week
- [ ] Monitor for errors
- [ ] Check analytics data
- [ ] Review user feedback
- [ ] Fix any issues

### First Month
- [ ] Add missing content
- [ ] Update outdated information
- [ ] Respond to community input
- [ ] Monitor search rankings

### Ongoing
- [ ] Update events regularly
- [ ] Add new businesses
- [ ] Incorporate new research
- [ ] Annual content review

---

## Time Estimates Summary

| Phase | Time |
|-------|------|
| Research | 1-2 weeks |
| Content Planning | 2-3 days |
| Site Setup | 1 day |
| Content Creation | 1-2 weeks |
| Data Population | 3-5 days |
| Visual Assets | 2-3 days |
| Testing | 1 day |
| Deployment | 1 day |
| Launch Verification | 1 day |
| **Total** | **4-6 weeks** |

---

## Parallel Execution Strategy

For building multiple sites, use parallel agents:

**Agent 1-4:** Historical research (different neighborhoods)
**Agent 5-8:** Content creation (different neighborhoods)
**Agent 9-12:** Data population (different neighborhoods)

Consolidate before deployment phase for batch operations.
