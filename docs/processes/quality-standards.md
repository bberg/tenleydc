# Quality Standards

> What makes content "complete" for a neighborhood site and how to verify quality.

---

## Content Completeness Criteria

### Essential Elements (Required)

| Element | Requirement | Verification |
|---------|-------------|--------------|
| Origin Story | Founding date, figure, etymology | Specific date mentioned |
| Historical Narrative | 3-5 development phases with dates | Each phase has date range |
| Geographic Boundaries | Street names in 4 cardinal directions | All 4 directions specified |
| Architectural Inventory | Primary styles, counts, specific addresses | At least 3 specific addresses |
| Institutions | Schools, churches, civic with dates | At least 5 institutions with founding dates |
| Transportation History | Coverage of each era | Wagon/streetcar/automobile/Metro |
| Demographic History | Racial composition, segregation, changes | Direct treatment of segregation |
| Contemporary Status | Current challenges and identity | Section dated within 2 years |

### Important Elements (Strongly Recommended)

| Element | Requirement | Verification |
|---------|-------------|--------------|
| Development Model | Developer names, plat dates, restrictions | Specific developer named |
| Archival Photos | 1+ historical images with attribution | Full LOC-style citation |
| Cross-References | Links to related pages | At least 3 internal links |
| Walking Guide | Key blocks and sites to visit | Specific addresses listed |
| Resources | Links to organizations | At least 3 external links |

---

## Writing Quality Standards

### Specificity Requirements

**Dates:**
- ✅ "July 11, 1864" or "In 1864"
- ❌ "In the early 1900s" or "around that time"

**Addresses:**
- ✅ "4001 Nebraska Avenue NW"
- ❌ "on Nebraska Avenue" or "in the area"

**Names:**
- ✅ "John Tennally" or "the W.C. & A.N. Miller Company"
- ❌ "a local tavern keeper" or "developers"

**Numbers:**
- ✅ "2,700 homes" or "409 feet elevation"
- ❌ "many homes" or "very high"

### Source Attribution

**Photos:**
- ✅ "Photo by Theodor Horydczak, Library of Congress, Prints and Photographs Division"
- ❌ "Historical photo" or no attribution

**Quotes:**
- ✅ Attribute to source with date/publication
- ❌ Unattributed quotations

**AI Images:**
- ✅ "*AI-generated artistic interpretation of [subject]. Not a historical photograph.*"
- ❌ Presenting AI images without disclosure

### Tone and Voice

**DO:**
- Write with authority based on research
- Explain technical details accessibly
- Address difficult history directly
- Include occasional appropriate humor
- Connect past to present

**DON'T:**
- Use vague language
- Minimize or euphemize racial history
- Include speculation without marking it
- Use academic jargon without explanation
- Ignore ongoing challenges

---

## Difficult History Standards

### Required Treatment

Content MUST address:
1. **Native American displacement** - Acknowledge original inhabitants
2. **Slavery connections** - If relevant to the area
3. **Racial segregation** - Restrictive covenants, discriminatory practices
4. **Community displacement** - Reno City, urban renewal, gentrification
5. **Environmental contamination** - WWI chemical weapons, etc.

### How to Address

**DO:**
- Name the practice (e.g., "restrictive racial covenants")
- Quote primary sources when available
- Specify who was affected
- Connect to larger patterns
- Acknowledge ongoing impact

**Example of proper treatment:**
> The 1928 deed restrictions specified that properties "shall not be sold to any person of the Semitic race, blood or origin which racial description can be deemed to include Jews, Hebrews, Armenians, Persians and Syrians."

**DON'T:**
- Use euphemisms ("housing restrictions")
- Minimize scope ("some discrimination")
- Present as isolated incident
- Omit specific details

---

## Data Quality Standards

### JSON Data Files

**Required fields for all entries:**
- `id` - Unique identifier
- `name` - Display name
- `slug` - URL-safe identifier
- `address` - Full street address

**Validation rules:**
- IDs must be unique across file
- Slugs must be lowercase, hyphenated
- Addresses must include "NW/NE/SW/SE"
- Phone numbers must be formatted consistently
- URLs must be valid and include https://

### History Fields

**When including history:**
- `opened` - Year as integer (1925, not "1925")
- `founded_by` - Full name of founder
- `story` - Minimum 2-3 sentences
- `what_was_here_before` - If known
- `neighborhood_context` - Connection to larger story

---

## Technical Quality Standards

### Performance

- Page load time: < 3 seconds on 3G
- Images: Optimized, < 500KB each
- CSS: Single file, minified in production
- JS: Single file, no framework dependencies

### Accessibility

- All images have alt text
- Color contrast meets WCAG AA
- Keyboard navigation works
- Screen reader compatible

### SEO

- Every page has unique title
- Meta descriptions on key pages
- Proper heading hierarchy (H1 → H2 → H3)
- Semantic HTML structure
- Sitemap.xml generated
- robots.txt configured

---

## Review Checklist

Before publishing new content:

### Content Review

- [ ] All essential elements present
- [ ] Dates are specific, not vague
- [ ] At least 5 specific addresses mentioned
- [ ] Difficult history addressed directly
- [ ] All sources attributed
- [ ] AI images labeled appropriately
- [ ] Cross-references to related pages
- [ ] Contemporary relevance established

### Data Review

- [ ] All required fields populated
- [ ] IDs and slugs are unique
- [ ] URLs tested and working
- [ ] Phone numbers formatted consistently
- [ ] History sections have minimum content

### Technical Review

- [ ] Page renders without errors
- [ ] Images load and are optimized
- [ ] Links work (no 404s)
- [ ] Mobile layout correct
- [ ] Search includes new content

### Final Verification

- [ ] Read full page aloud (catches awkward phrasing)
- [ ] Verify every fact against source
- [ ] Check for any vague language
- [ ] Confirm difficult history coverage
- [ ] Test all interactive elements

---

## Quality Metrics

### Content Depth Targets

| Content Type | Word Count Target | Minimum Acceptable |
|--------------|-------------------|-------------------|
| Neighborhood Deep Dive | 4,000-5,000 | 3,000 |
| Institution Focus | 7,000-8,000 | 5,000 |
| Thematic Overview | 7,000-8,500 | 5,500 |
| Site-Specific | 9,000-10,000 | 7,000 |
| Comparative/Reference | 8,000-9,000 | 6,000 |
| Practical Guide | 6,000-8,000 | 4,500 |

### Research Depth Indicators

**High Quality:**
- Uses primary sources (newspapers, archives)
- Includes specific quotes from era
- Cites multiple sources per section
- Includes lesser-known details
- Recent research incorporated

**Adequate Quality:**
- Uses secondary sources (books, articles)
- General historical narrative
- Basic facts verified
- Standard details included

**Insufficient Quality:**
- Relies on Wikipedia only
- Vague generalizations
- Unverified claims
- Missing major topics

---

## Continuous Improvement

### Post-Publication Review

After 30 days:
- Review analytics for engagement
- Check for user corrections
- Update any outdated information
- Add newly discovered sources

### Annual Review

- Verify all external links
- Update demographic data
- Add recent historical findings
- Refresh contemporary sections
- Check for new archival materials

### User Feedback Integration

- Track submitted corrections
- Document enhancement requests
- Prioritize based on impact
- Credit community contributors
