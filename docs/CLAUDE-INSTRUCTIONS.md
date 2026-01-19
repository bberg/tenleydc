# Instructions for Claude Code

> Copy this file and the workflow docs to your new project. This README tells Claude what to do.

---

## Context

We're building a network of sites. One site has already been built extensively - use it as the reference pattern for building additional sites.

## Workflow Documentation

The `docs/workflow/` directory contains the infrastructure workflow:
- Domain identification, purchase, DNS
- Deployment (Railway, Cloudflare, GitHub)
- Site template structure
- Analytics and monitoring
- SEO implementation

**Follow these docs for all infrastructure tasks.**

## Critical Requirements

### 1. Document Your Processes

As you build each new site, **carefully document every process you use** in `docs/processes/`.

Before building additional sites, look back at the first site you built:
- What steps did you take?
- What research did you do?
- What sources did you use?
- What patterns emerged?
- What worked well? What didn't?

Create detailed documentation of these processes so they can be replicated without needing to re-explain everything.

Example files to create:
```
docs/processes/
├── research-workflow.md      # How you gather information for each site
├── content-structure.md      # How content is organized
├── data-sources.md           # Where information comes from
├── quality-checks.md         # How you verify accuracy
└── lessons-learned.md        # What to do/avoid
```

### 2. No Content Copying

Each site in this network must have **completely original content**. Do not copy text, descriptions, or content patterns from unrelated projects.

### 3. Consistency Across Sites

While content is unique per site, maintain consistency in:
- Technical infrastructure (use the workflow docs)
- Site structure and navigation patterns
- Design and UX patterns
- SEO implementation

### 4. Self-Document as You Go

Every time you develop a new process or solve a problem:
1. Document it immediately in `docs/processes/`
2. Be specific enough that you (or another Claude) could follow the same steps
3. Include examples where helpful

---

## Getting Started Prompt

When starting work on additional sites, begin with:

```
Review the existing site we've built to understand the patterns and processes used.
Document what you find in docs/processes/ before building new sites.
Then follow docs/workflow/ for infrastructure setup.
```

---

## Files to Copy to New Project

```
docs/
├── workflow/                    # Copy entire workflow-generic folder, rename to workflow
│   ├── 00-WORKFLOW-OVERVIEW.md
│   ├── 01-DOMAIN-IDENTIFICATION.md
│   ├── 02-DOMAIN-PURCHASE-DNS.md
│   ├── 03-DEPLOYMENT-INFRASTRUCTURE.md
│   ├── 04-SITE-TEMPLATE-STRUCTURE.md
│   ├── 05-ANALYTICS-MONITORING.md
│   └── 06-SEO-IMPLEMENTATION.md
├── processes/                   # Create empty, Claude will populate
└── README-FOR-NEW-PROJECT.md    # This file (can rename to CLAUDE-INSTRUCTIONS.md)

shared/tools/                    # Copy deployment automation
├── deploy/
└── domain/
```
