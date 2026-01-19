# Phase 1: Domain Identification

> A systematic process for researching, generating, and selecting domains for a multi-site network.

## Overview

Domain identification involves three key steps:
1. **Brainstorming** - Generate domain ideas based on site purpose
2. **Availability Checking** - Verify domains are available
3. **Selection & Ranking** - Choose the best options with backups

## Step 1: Define Your Sites

Before searching for domains, clearly define each site in your network:

```markdown
| Site Name | Purpose | Target Keywords | Target Audience |
|-----------|---------|-----------------|-----------------|
| Site 1    | ...     | keyword1, kw2   | Audience desc   |
| Site 2    | ...     | keyword1, kw2   | Audience desc   |
```

### Document This Step

Create `docs/processes/site-definitions.md` with:
- Full list of planned sites
- Purpose and scope of each
- Target audience profiles
- How sites relate to each other

## Step 2: Domain Brainstorming Strategies

### Strategy A: Keyword-Based Domains
Direct SEO value, immediately clear purpose.

**Pattern:** `[keyword][modifier].com`
- Example: `[topic]guide.com`, `[location]info.com`

**Pros:** SEO-friendly, clear purpose
**Cons:** Often taken, longer names

### Strategy B: Brandable Domains
Shorter, memorable, unique identity.

**Pattern:** `[evocative-word][suffix].com`
- Example: Creative coined words, metaphors

**Pros:** Memorable, shorter, available
**Cons:** Less SEO signal, meaning needs establishment

### Strategy C: Hybrid Approach (Recommended)
Combine a key term with a brand element.

**Pattern:** `[partial-keyword][brand].com`
- Example: `[topic]hq.com`, `[topic]hub.com`

## Step 3: Generate Domain Candidates

### Method 1: Claude Code Assistance

Ask Claude to generate domain ideas:

```
Generate 20 domain name suggestions for a [SITE PURPOSE] website.
Requirements:
- .com TLD preferred
- Under 15 characters
- Mix of keyword-based and brandable options
- Avoid hyphens and numbers
```

### Method 2: Automated Generation (GPT + API)

Use the domain search script to generate and check domains:

```bash
cd shared/tools
python domain_search.py
```

**Script Capabilities:**
1. Uses GPT to generate domain suggestions based on topic
2. Checks availability via Domainr API
3. Ranks available domains by quality
4. Optionally saves results to Notion

### Method 3: Manual Brainstorming Matrix

Create a word matrix and combine:

| Prefix | Root | Suffix | Result |
|--------|------|--------|--------|
| [word] | [topic] | .com | example.com |

## Step 4: Check Availability

### Option A: Quick CLI Check

```bash
python shared/tools/check_availability.py domain1.com domain2.com domain3.com
```

Output:
```
domain1.com: ['inactive'] ✅ AVAILABLE
domain2.com: ['active'] ❌ taken
```

### Option B: Domainr API (Programmatic)

```python
import requests

def check_domain(domain, api_key):
    url = "https://domainr.p.rapidapi.com/v2/status"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "domainr.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params={"domain": domain})
    data = response.json()

    if "status" in data and data["status"]:
        status = data["status"][0].get("status", [])
        # Available: 'inactive', 'undelegated'
        # Taken: 'active', 'registered'
        return status
    return ["unknown"]
```

### Option C: Manual Check (Fallback)

Visit registrars directly:
- [Cloudflare Registrar](https://dash.cloudflare.com/domains)
- [Namecheap](https://www.namecheap.com/)
- [Google Domains](https://domains.google/)

## Step 5: Evaluate & Rank Domains

### Scoring Criteria

| Factor | Weight | Description |
|--------|--------|-------------|
| Length | 20% | Shorter is better (ideal: 8-12 chars) |
| Memorability | 25% | Easy to spell, say, remember |
| SEO Value | 20% | Contains target keywords |
| Brandability | 20% | Unique, ownable identity |
| TLD Quality | 15% | .com > .co > .io > others |

### Evaluation Template

```markdown
## Domain: [example.com]

| Factor | Score (1-5) | Notes |
|--------|-------------|-------|
| Length | 4 | 11 characters - good |
| Memorability | 5 | Easy to spell and say |
| SEO Value | 3 | Partial keyword match |
| Brandability | 4 | Unique and ownable |
| TLD | 5 | .com domain |
| **Total** | **21/25** | Strong candidate |
```

### Comparison Matrix

```markdown
| Domain | Length | Memory | SEO | Brand | TLD | Total | Rank |
|--------|--------|--------|-----|-------|-----|-------|------|
| domain1.com | 4 | 5 | 3 | 4 | 5 | 21 | 1 |
| domain2.com | 3 | 4 | 5 | 2 | 3 | 17 | 3 |
```

## Step 6: Finalize Selection

### Document Final Choices

Create `docs/domains/domains-final.md`:

```markdown
# Final Domain Selections

| Site | Primary Domain | Backup Domain | Rationale |
|------|----------------|---------------|-----------|
| Site1 | domain1.com | backup1.com | [Why this domain] |
| Site2 | domain2.com | backup2.com | [Why this domain] |

## Registration Checklist
- [ ] domain1.com
- [ ] domain2.com
...

## Estimated Cost
[N] domains × $12/year = ~$[total]/year
```

### Backup Strategy

Always identify 1-2 backup domains for each site in case:
- Primary is taken before you register
- Future brand protection needs
- Alternative branding direction

## Tools Reference

### Files to Set Up

```
shared/tools/
├── domain_search.py       # GPT + Domainr full pipeline
├── check_availability.py  # Quick CLI availability check
└── domain_search_api.py   # Alternative API client
```

### API Requirements

```bash
# In .env file
OPENAI_API_KEY=sk-...      # For GPT domain generation
RAPIDAPI_KEY=...           # For Domainr availability API
```

### Getting RapidAPI Key

1. Sign up at [RapidAPI](https://rapidapi.com/)
2. Subscribe to [Domainr API](https://rapidapi.com/domainr/api/domainr/)
3. Copy your API key from the dashboard

## Claude Code Integration

### Prompt for Domain Research

```
I need domains for a network of [N] sites about [TOPIC].

Sites and purposes:
1. [Site1]: [purpose]
2. [Site2]: [purpose]
...

For each site, suggest:
- 3 keyword-based domains
- 3 brandable domains
- Reasoning for each suggestion

Then check availability using shared/tools/check_availability.py

Document your research process in docs/processes/domain-research.md
```

### Prompt for Final Selection

```
Review the available domains we found:

[List of available domains]

For each site, recommend:
1. Primary domain (with rationale)
2. Backup domain (with rationale)

Consider: length, memorability, SEO value, brandability, TLD quality
```

## Process Documentation

After completing domain identification, document your process:

**Create:** `docs/processes/domain-research.md`
- What search terms worked best
- Which domain patterns are available in your niche
- Lessons learned for future domain searches
- Tools and APIs that worked well

## Output Checklist

After completing domain identification, you should have:

- [ ] List of all sites with purposes defined
- [ ] 5-10 candidate domains per site
- [ ] Availability status for all candidates
- [ ] Scored/ranked evaluation of available domains
- [ ] Final selection document with primary + backup per site
- [ ] Cost estimate for registration
- [ ] Process documented for future reference

---

**Next Step:** [02-DOMAIN-PURCHASE-DNS.md](./02-DOMAIN-PURCHASE-DNS.md)
