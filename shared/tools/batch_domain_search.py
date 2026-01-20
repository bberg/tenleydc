#!/usr/bin/env python3
"""
Batch domain search for all neighborhood history sites.
Generates 100 domain ideas per neighborhood, checks availability, ranks best ones.
"""
import os
import sys
import time
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv('/Users/bb/www/audio-tools-network/.env')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '').strip().strip('"')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '').strip().strip('"')

HEADERS = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': 'domainr.p.rapidapi.com'
}

# All 16 neighborhoods
NEIGHBORHOODS = [
    {"name": "Tenleytown", "slug": "tenleytown", "state": "DC", "context": "historic DC neighborhood near AU, Tenley Circle, Fort Reno"},
    {"name": "Brightwood", "slug": "brightwood", "state": "DC", "context": "Fort Stevens, Civil War history, African American heritage"},
    {"name": "Kalorama", "slug": "kalorama", "state": "DC", "context": "embassy row, 5 presidents lived here, Gilded Age mansions"},
    {"name": "College Park", "slug": "college-park", "state": "MD", "context": "University of Maryland, world's oldest airport"},
    {"name": "Hyattsville", "slug": "hyattsville", "state": "MD", "context": "arts district, historic downtown, streetcar suburb"},
    {"name": "Potomac", "slug": "potomac", "state": "MD", "context": "wealthy suburb, Great Falls, C&O Canal history"},
    {"name": "Falls Church", "slug": "falls-church", "state": "VA", "context": "Little City, colonial history, Civil War"},
    {"name": "Vienna", "slug": "vienna", "state": "VA", "context": "W&OD Railroad, Civil War, small town charm"},
    {"name": "Del Ray", "slug": "del-ray", "state": "VA", "context": "Alexandria neighborhood, arts community, Avenue style"},
    {"name": "Columbia Heights", "slug": "columbia-heights", "state": "DC", "context": "1968 riots, historic theaters, Latino culture"},
    {"name": "H Street", "slug": "h-street", "state": "DC", "context": "Atlas District, streetcar, music venues, revitalization"},
    {"name": "SW Waterfront", "slug": "sw-waterfront", "state": "DC", "context": "The Wharf, urban renewal, fish market history"},
    {"name": "Anacostia", "slug": "anacostia", "state": "DC", "context": "Frederick Douglass, African American history, Anacostia River"},
    {"name": "Shepherd Park", "slug": "shepherd-park", "state": "DC", "context": "integration history, Neighbors Inc, Jewish community"},
    {"name": "Glover Park", "slug": "glover-park", "state": "DC", "context": "near Georgetown, Glover Archbold Park, neighborhood village"},
    {"name": "Woodley Park", "slug": "woodley-park", "state": "DC", "context": "National Zoo, Wardman Park, historic apartments"},
]


def generate_domain_suggestions(neighborhood):
    """Generate 100 creative domain ideas for a neighborhood."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""Generate 100 creative, brandable domain name suggestions for a local history and community website about {neighborhood['name']}, {neighborhood['state']}.

Context: {neighborhood['context']}

The site will cover neighborhood history, local stories, community events, and local culture - similar to a neighborhood almanac or chronicle.

Generate diverse suggestions including:
- History-focused: e.g., {neighborhood['slug']}history.com, historic{neighborhood['slug']}.com
- Chronicle/stories: e.g., {neighborhood['slug']}chronicle.com, {neighborhood['slug']}stories.com
- Almanac style: e.g., {neighborhood['slug']}almanac.com
- Community: e.g., {neighborhood['slug']}life.com, my{neighborhood['slug']}.com
- News/media: e.g., {neighborhood['slug']}times.com, {neighborhood['slug']}post.com
- Discovery: e.g., discover{neighborhood['slug']}.com
- Hub/connection: e.g., {neighborhood['slug']}hub.com
- Geographic variants: e.g., {neighborhood['slug']}dc.com, {neighborhood['slug']}md.com
- Creative/unique: memorable brandable names related to the area
- Short memorable names
- Names that would rank well for "{neighborhood['name']} history" searches

Include .com, .org, .net, .co variations for the best ideas.
One domain per line, no numbering or commentary."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    suggestions_raw = response.choices[0].message.content.split("\n")
    suggestions = [s.strip().lower() for s in suggestions_raw if s.strip() and '.' in s]
    return suggestions[:100]  # Ensure max 100


def check_availability(domain):
    """Check if domain is available via Domainr API."""
    url = 'https://domainr.p.rapidapi.com/v2/status'
    params = {'domain': domain}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                status_info = data['status'][0]
                status_str = status_info.get('status', '')
                summary = status_info.get('summary', '')
                is_available = 'inactive' in status_str or 'undelegated' in status_str
                return {
                    'domain': domain,
                    'available': is_available,
                    'status': status_str,
                    'summary': summary
                }
        return {'domain': domain, 'available': False, 'status': 'error', 'summary': 'API error'}
    except Exception as e:
        return {'domain': domain, 'available': False, 'status': 'error', 'summary': str(e)}


def rank_domains(neighborhood, available_domains):
    """Use GPT to rank available domains by quality."""
    if not available_domains:
        return []

    client = OpenAI(api_key=OPENAI_API_KEY)
    domain_list = "\n".join(f"- {d['domain']}" for d in available_domains)

    prompt = f"""Rank these available domain names for a {neighborhood['name']} local history website.

Context: {neighborhood['context']}

Available domains:
{domain_list}

Rank from best to worst based on:
1. Memorability and brandability
2. SEO potential for "{neighborhood['name']} history" searches
3. Professional appearance
4. Short length preferred
5. .com preferred over other TLDs

Return ONLY the domains, one per line, best first. No commentary."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    ranked = [s.strip().lower() for s in response.choices[0].message.content.split("\n") if s.strip() and '.' in s]
    return ranked


def save_results(neighborhood, suggestions, available, ranked, output_dir):
    """Save results to markdown file."""
    filepath = os.path.join(output_dir, f"{neighborhood['slug']}-domains.md")

    with open(filepath, 'w') as f:
        f.write(f"# Domain Research: {neighborhood['name']}, {neighborhood['state']}\n\n")
        f.write(f"**Context:** {neighborhood['context']}\n\n")
        f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")

        f.write(f"## Summary\n\n")
        f.write(f"- **Total suggestions:** {len(suggestions)}\n")
        f.write(f"- **Available:** {len(available)}\n")
        f.write(f"- **Taken:** {len(suggestions) - len(available)}\n\n")

        if ranked:
            f.write("## Top Available Domains (Ranked)\n\n")
            f.write("| Rank | Domain | Status |\n")
            f.write("|------|--------|--------|\n")
            for i, domain in enumerate(ranked[:20], 1):
                f.write(f"| {i} | **{domain}** | ✅ Available |\n")
            f.write("\n")

        if available:
            f.write("## All Available Domains\n\n")
            for d in available:
                f.write(f"- ✅ {d['domain']}\n")
            f.write("\n")

        f.write("## Checked Domains (Full List)\n\n")
        f.write("| Domain | Status |\n")
        f.write("|--------|--------|\n")
        for s in suggestions[:100]:
            # Find status
            avail = next((a for a in available if a['domain'] == s), None)
            if avail:
                f.write(f"| {s} | ✅ Available |\n")
            else:
                f.write(f"| {s} | ❌ Taken |\n")

    return filepath


def process_neighborhood(neighborhood, output_dir):
    """Process a single neighborhood - generate, check, rank, save."""
    print(f"\n{'='*60}")
    print(f"Processing: {neighborhood['name']}, {neighborhood['state']}")
    print(f"{'='*60}")

    # Step 1: Generate suggestions
    print(f"  Generating 100 domain suggestions...")
    suggestions = generate_domain_suggestions(neighborhood)
    print(f"  Generated {len(suggestions)} suggestions")

    # Step 2: Check availability (with rate limiting)
    print(f"  Checking availability...")
    available = []
    for i, domain in enumerate(suggestions):
        result = check_availability(domain)
        if result['available']:
            available.append(result)
            print(f"    ✅ {domain}")
        if (i + 1) % 10 == 0:
            print(f"    Checked {i+1}/{len(suggestions)}...")
            time.sleep(0.5)  # Rate limiting

    print(f"  Found {len(available)} available domains")

    # Step 3: Rank available domains
    ranked = []
    if available:
        print(f"  Ranking available domains...")
        ranked = rank_domains(neighborhood, available)
        print(f"  Top 5: {', '.join(ranked[:5])}")

    # Step 4: Save results
    filepath = save_results(neighborhood, suggestions, available, ranked, output_dir)
    print(f"  Saved to: {filepath}")

    return {
        'neighborhood': neighborhood['name'],
        'suggestions': len(suggestions),
        'available': len(available),
        'top_domain': ranked[0] if ranked else None,
        'top_5': ranked[:5] if ranked else []
    }


def main():
    output_dir = '/Users/bb/www/au-park-history/research/domains'
    os.makedirs(output_dir, exist_ok=True)

    # Process specific neighborhood if provided, otherwise all
    if len(sys.argv) > 1:
        slug = sys.argv[1]
        neighborhoods = [n for n in NEIGHBORHOODS if n['slug'] == slug]
        if not neighborhoods:
            print(f"Unknown neighborhood: {slug}")
            sys.exit(1)
    else:
        neighborhoods = NEIGHBORHOODS

    print(f"Processing {len(neighborhoods)} neighborhoods...")

    results = []
    for neighborhood in neighborhoods:
        result = process_neighborhood(neighborhood, output_dir)
        results.append(result)

    # Save summary
    summary_path = os.path.join(output_dir, 'DOMAIN-SUMMARY.md')
    with open(summary_path, 'w') as f:
        f.write("# Domain Research Summary\n\n")
        f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Best Available Domains by Neighborhood\n\n")
        f.write("| Neighborhood | Top Domain | Available Count | Top 5 |\n")
        f.write("|--------------|------------|-----------------|-------|\n")
        for r in results:
            top5 = ', '.join(r['top_5'][:3]) if r['top_5'] else 'None'
            f.write(f"| {r['neighborhood']} | **{r['top_domain'] or 'None'}** | {r['available']} | {top5} |\n")

    print(f"\n{'='*60}")
    print(f"COMPLETE! Summary saved to: {summary_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
