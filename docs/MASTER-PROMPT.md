# Master Prompt: DMV Neighborhood Sites Network

> Copy everything below the line to give to Claude in this project.

---

## Project Overview

We are building a network of **15+ neighborhood history and community sites** for the DMV region (Washington DC, Maryland, Virginia).

**We have already built one site extensively: AU Park (American University Park).** This existing site is your reference pattern. Before building any new sites, you MUST analyze this existing site and document the processes used to create it.

## Critical First Step: Document the Existing Process

**BEFORE doing anything else**, thoroughly review the existing AU Park site:

1. **Examine all content files** in `content/` - understand the structure, depth, topics covered
2. **Review the scraper** in `scraper/` - understand data collection methods
3. **Look at plans/** - understand the roadmap and thinking
4. **Check existing docs/** - review market-research.md, rebrand-plan.md
5. **Examine the site structure** - templates, static files, app.py, etc.

Then **create comprehensive documentation** in `docs/processes/` capturing:

```
docs/processes/
├── market-research-process.md     # How to research competitors, existing sites, market gaps
├── content-research-process.md    # How content was researched and gathered
├── content-structure.md           # How content is organized (what sections, what depth)
├── data-sources.md                # What sources were used (archives, libraries, APIs, etc.)
├── site-architecture.md           # Technical structure of each site
├── quality-standards.md           # What makes content "complete" for a neighborhood
└── replication-checklist.md       # Step-by-step to replicate for new neighborhood
```

**This documentation phase is NON-NEGOTIABLE.** Do not proceed to building new sites until this is complete and thorough.

## Flexibility Principle: Each Neighborhood Is Unique

**Important:** While we want consistency in infrastructure and quality, each neighborhood site should reflect its unique character:

### Content Flexibility
- **Different sections for different neighborhoods** - Not every neighborhood has the same story. One might have rich military history (Fort Reno), another might be defined by its university (AU Park), another by its commercial district or architecture.
- **Navigation varies by relevance** - If a neighborhood doesn't have notable broadcasting history, don't include that nav item. If it has a famous cemetery or park, add that section.
- **Depth varies by available content** - Some neighborhoods have extensive archives; others don't. Quality over forced quantity.

### Style Flexibility (Subtle)
- **Color accents can reflect neighborhood vibe** - A historic Georgetown might feel different than an artsy Adams Morgan. Adjust accent colors, not wholesale redesigns.
- **Keep core layout consistent** - Same basic structure, typography system, and UX patterns across all sites.
- **Don't go overboard** - Subtle variations, not completely different designs. They should feel like a family of sites.

### What This Means for Process Documentation
When documenting the content structure in `docs/processes/content-structure.md`, document:
- **Required sections** (every site needs these)
- **Optional sections** (include if relevant to the neighborhood)
- **How to decide** what sections a neighborhood needs based on research

## Infrastructure Workflow

For all technical/infrastructure tasks, follow the documentation in `docs/workflow/`:
- Domain identification and purchase
- DNS and SSL configuration
- Railway deployment
- Analytics and monitoring
- SEO implementation

Also read `docs/CLAUDE-INSTRUCTIONS.md` for additional context.

## Target Neighborhoods (15 Sites)

We need sites for these DMV neighborhoods. Prioritize based on your research into which have:
- Rich historical content available
- Active community interest
- Good domain availability

**Washington DC neighborhoods:**
- AU Park (DONE - reference site)
- Tenleytown
- Cleveland Park
- Friendship Heights
- Chevy Chase DC
- Georgetown
- Dupont Circle
- Adams Morgan
- Capitol Hill
- Brookland

**Maryland:**
- Bethesda
- Silver Spring
- Takoma Park
- College Park

**Virginia:**
- Arlington (Clarendon/Ballston corridor)
- Alexandria (Old Town)

Adjust this list based on your research. Some neighborhoods may have better content availability than others.

---

## UNLEASH SUB-AGENTS: Parallel Execution Strategy

You have access to the **Task tool** with specialized sub-agents. USE THEM AGGRESSIVELY to parallelize work. Do not do sequentially what can be done in parallel.

### Phase 1: Documentation & Analysis (Use Explore Agents)

Launch **multiple Explore agents in parallel** to analyze the existing site:

```
Launch these agents SIMULTANEOUSLY:

Agent 1: "Analyze all content files in content/*.md - document the structure, sections,
         depth of coverage, writing style, and create a content template"

Agent 2: "Analyze the scraper/ directory - document what data sources are being scraped,
         how data is processed, and what the collection methodology is"

Agent 3: "Analyze the site architecture - app.py, templates/, static/ - document the
         technical structure and how content flows to the frontend"

Agent 4: "Review docs/ and plans/ - synthesize the strategic thinking, market research,
         and roadmap into a summary document"

Agent 5: "Analyze docs/market-research.md in detail - document the market research
         methodology: what competitors were researched, what data was gathered,
         how gaps/opportunities were identified. Create a replicable market research
         template in docs/processes/market-research-process.md"
```

### Phase 2: Market Research (Use WebSearch Agents)

**BEFORE creating content**, conduct market research for each neighborhood to understand:
- What sites already exist for this neighborhood?
- Who are the competitors (local blogs, historical societies, community sites)?
- What content gaps exist that we can fill?
- What's the community's online presence like?

```
Launch parallel WebSearch agents for batches of neighborhoods:

Agent 1: "Conduct market research for [Neighborhood A]:
         - Search for existing neighborhood websites, blogs, community sites
         - Find historical societies, civic associations, local news coverage
         - Identify social media presence (@neighborhood handles, Facebook groups)
         - Document competitors, their strengths/weaknesses, and content gaps
         - Save findings to research/[neighborhood-a]/market-research.md
         Follow the methodology documented in docs/processes/market-research-process.md"

Agent 2: "Conduct market research for [Neighborhood B]..." (same pattern)

Agent 3: "Conduct market research for [Neighborhood C]..." (same pattern)

Agent 4: "Conduct market research for [Neighborhood D]..." (same pattern)
```

### Phase 3: Historical & Content Research (Use Explore + WebSearch Agents)

For each new neighborhood, launch **parallel research agents**:

```
For neighborhoods [A, B, C, D] simultaneously:

Agent A: "Research [Neighborhood A] history, landmarks, demographics, notable residents.
         Find primary sources: historical societies, library archives, government records.
         Document findings and sources in research/[neighborhood-a]/historical-research.md"

Agent B: "Research [Neighborhood B]..." (same pattern)

Agent C: "Research [Neighborhood C]..." (same pattern)

Agent D: "Research [Neighborhood D]..." (same pattern)
```

### Phase 4: Domain Selection (Parallel Availability Checks)

```
Launch agent: "For all 15 neighborhoods, generate domain name candidates and check
              availability using shared/tools/. Run availability checks in parallel.
              Document results in docs/domains/availability-matrix.md"
```

### Phase 5: Content Generation (Parallel Content Creation)

Once research is complete, generate content in parallel. **Each neighborhood gets tailored content based on its unique story:**

```
For neighborhoods with completed research, launch parallel agents:

Agent 1: "Using docs/processes/content-structure.md as a guide (not rigid template),
         and the research in research/[neighborhood]/:
         1. Determine which sections are relevant for THIS neighborhood based on research
         2. Generate content files for sections that matter here
         3. Skip sections that aren't relevant (don't force content that doesn't exist)
         4. Add unique sections if this neighborhood has something special
         5. Note any style/vibe considerations for this neighborhood
         Output: content files + a site-plan.md noting which sections and why"

Agent 2: (same for different neighborhood)
Agent 3: (same for different neighborhood)
Agent 4: (same for different neighborhood)
```

**Remember:** Georgetown's nav might include "Historic Estates" while Adams Morgan's includes "Music Scene." Don't force uniformity.

### Phase 6: Site Scaffolding (Parallel Site Creation)

```
Launch parallel agents to create site directories:

Agent 1: "Create the full site structure for [neighborhood-1]:
         1. Start from site-template base
         2. Customize navigation based on site-plan.md (which sections exist)
         3. Apply subtle style variations if noted (accent colors, etc.)
         4. Set up app.py with routes for THIS site's sections
         5. Configure templates, static files, railway.toml, requirements.txt
         The site should feel part of the family but reflect its neighborhood's character"

Agent 2-N: (same pattern for other neighborhoods)
```

### Phase 7: Deployment (Batch Operations)

```
Launch agent: "Using shared/tools/deploy/, deploy all completed sites in batch:
              1. Create GitHub repos for all sites
              2. Create Railway projects for all sites
              3. Configure Cloudflare DNS for all domains
              4. Set up GA4 properties for all sites
              5. Inject analytics into all sites"
```

---

## Execution Rules

### DO:
- Launch multiple sub-agents simultaneously whenever tasks are independent
- Use Explore agents for codebase analysis and research
- Use background tasks for long-running operations
- Document EVERYTHING in docs/processes/ as you discover patterns
- Create reusable templates based on the AU Park site
- Check in on background agents periodically

### DO NOT:
- Do tasks sequentially that could be parallelized
- Start building new sites before documenting the existing process
- Copy content verbatim between neighborhoods - each must be unique
- Skip the research phase - quality content requires quality research
- Forget to document your processes as you develop them

### Sub-Agent Best Practices:
- Give agents SPECIFIC, BOUNDED tasks
- Include file paths and expected outputs in agent prompts
- Launch 3-5 agents in parallel for major phases
- Use "run_in_background" for tasks that take time
- Consolidate agent outputs before moving to next phase

---

## Directory Structure to Create

```
au-park-history/                    # Existing - rename to dmv-neighborhoods or similar
├── docs/
│   ├── CLAUDE-INSTRUCTIONS.md
│   ├── MASTER-PROMPT.md           # This file
│   ├── workflow/                   # Infrastructure workflow (copied)
│   ├── processes/                  # YOU CREATE THIS - document everything
│   └── domains/                    # Domain research and selections
├── shared/
│   └── tools/                      # Deployment automation (copied)
├── research/                       # Research per neighborhood
│   ├── au-park/
│   │   ├── market-research.md      # Competitor analysis, gaps, opportunities
│   │   └── historical-research.md  # History, landmarks, sources
│   ├── tenleytown/
│   │   ├── market-research.md
│   │   └── historical-research.md
│   ├── cleveland-park/
│   └── .../
├── sites/                          # Individual site directories
│   ├── au-park/                    # Existing site (move here)
│   ├── tenleytown/
│   ├── cleveland-park/
│   └── .../
├── site-template/                  # Template extracted from AU Park
└── site-monitor/                   # Monitoring agent for all sites
```

---

## Success Metrics

By the end of this project:

- [ ] docs/processes/ contains 6+ detailed process documents including market research methodology
- [ ] Market research completed for all 15 neighborhoods (competitors, gaps, opportunities)
- [ ] Historical/content research completed for all 15 neighborhoods with sources documented
- [ ] 15 domains identified and purchased
- [ ] 15 sites with complete, unique content
- [ ] All sites deployed to Railway with custom domains
- [ ] All sites have GA4 tracking
- [ ] All sites verified in Search Console
- [ ] Site monitor tracking all 15+ sites
- [ ] Total process documented well enough that another Claude could replicate it

---

## Get Started

Begin with this command:

```
Read docs/CLAUDE-INSTRUCTIONS.md and docs/workflow/00-WORKFLOW-OVERVIEW.md to understand
the infrastructure workflow.

Then, launch 5 parallel Explore agents to analyze the existing AU Park site:
1. Content analysis (content/*.md)
2. Scraper/data collection analysis (scraper/)
3. Site architecture analysis (app.py, templates/, static/)
4. Strategic docs analysis (docs/, plans/)
5. Market research methodology analysis (docs/market-research.md) - document HOW the
   market research was conducted so we can replicate it for other neighborhoods

Synthesize their findings into comprehensive process documentation in docs/processes/.
The market research process documentation is CRITICAL - we need to understand competitors
and gaps for EVERY neighborhood before creating content.

Do not proceed to building new sites until the documentation phase is complete.
```

---

## Notes

- The existing AU Park site is your gold standard - understand it deeply
- Quality over speed - but use parallelization to get quality AND speed
- Every process you figure out should be documented for replication
- This is a NETWORK of sites - they should cross-link and share infrastructure
- The docs/workflow/ covers the technical infrastructure - follow it
- YOU figure out the content/research methodology from the existing site
