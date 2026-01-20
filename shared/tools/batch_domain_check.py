#!/usr/bin/env python3
"""
Batch domain availability checker for neighborhood history sites.
Generates domain patterns and checks availability via Domainr API.
"""
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv('/Users/bb/www/audio-tools-network/.env')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '').strip().strip('"')

HEADERS = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': 'domainr.p.rapidapi.com'
}

# All 16 neighborhoods with variants
NEIGHBORHOODS = [
    {"name": "Tenleytown", "slug": "tenleytown", "variants": ["tenleytown", "tenley", "tennallys", "tennally"], "state": "dc"},
    {"name": "Brightwood", "slug": "brightwood", "variants": ["brightwood", "brightwooddc", "brightwoodpark"], "state": "dc"},
    {"name": "Kalorama", "slug": "kalorama", "variants": ["kalorama", "kaloramadc", "kaloramaheights"], "state": "dc"},
    {"name": "College Park", "slug": "college-park", "variants": ["collegepark", "cparkmd", "collegeparkmd"], "state": "md"},
    {"name": "Hyattsville", "slug": "hyattsville", "variants": ["hyattsville", "hyattsvillemd", "oldtownhyattsville"], "state": "md"},
    {"name": "Potomac", "slug": "potomac", "variants": ["potomac", "potomacmd", "potomacvillage"], "state": "md"},
    {"name": "Falls Church", "slug": "falls-church", "variants": ["fallschurch", "fallschurchva", "littlecity", "thelittlecity"], "state": "va"},
    {"name": "Vienna", "slug": "vienna", "variants": ["vienna", "viennava", "viennatown"], "state": "va"},
    {"name": "Del Ray", "slug": "del-ray", "variants": ["delray", "delrayva", "delrayalexandria"], "state": "va"},
    {"name": "Columbia Heights", "slug": "columbia-heights", "variants": ["columbiaheights", "cohi", "cohidc"], "state": "dc"},
    {"name": "H Street", "slug": "h-street", "variants": ["hstreet", "hstreetne", "hstcorridor", "atlasdistrict"], "state": "dc"},
    {"name": "SW Waterfront", "slug": "sw-waterfront", "variants": ["swwaterfront", "swdc", "thewharfdc", "waterfront"], "state": "dc"},
    {"name": "Anacostia", "slug": "anacostia", "variants": ["anacostia", "anacostiadc", "historicancostia"], "state": "dc"},
    {"name": "Shepherd Park", "slug": "shepherd-park", "variants": ["shepherdpark", "shepherdparkdc"], "state": "dc"},
    {"name": "Glover Park", "slug": "glover-park", "variants": ["gloverpark", "gloverparkdc"], "state": "dc"},
    {"name": "Woodley Park", "slug": "woodley-park", "variants": ["woodleypark", "woodleyparkdc", "woodley"], "state": "dc"},
]

# Domain name patterns - {name} will be replaced with neighborhood variants
PATTERNS = [
    # History/Heritage
    "{name}history.com",
    "{name}history.org",
    "historic{name}.com",
    "historic{name}.org",
    "{name}heritage.com",
    "{name}heritage.org",
    "{name}past.com",
    "{name}then.com",
    "{name}thenandnow.com",

    # Almanac/Chronicle/Stories
    "{name}almanac.com",
    "{name}almanac.org",
    "{name}chronicle.com",
    "{name}chronicle.org",
    "{name}stories.com",
    "{name}stories.org",
    "{name}tales.com",
    "{name}memories.com",

    # Community/Local
    "{name}life.com",
    "{name}living.com",
    "{name}local.com",
    "{name}community.com",
    "my{name}.com",
    "our{name}.com",
    "{name}neighbors.com",
    "{name}neighbor.com",

    # News/Media
    "{name}times.com",
    "{name}times.org",
    "{name}post.com",
    "{name}gazette.com",
    "{name}observer.com",
    "{name}voice.com",
    "{name}news.com",
    "{name}bulletin.com",

    # Discovery/Exploration
    "discover{name}.com",
    "explore{name}.com",
    "visit{name}.com",
    "about{name}.com",

    # Hub/Connection
    "{name}hub.com",
    "{name}central.com",
    "{name}connect.com",
    "{name}connection.com",

    # Online presence
    "{name}online.com",
    "{name}guide.com",
    "{name}info.com",
    "{name}site.com",
    "{name}.info",
    "{name}.co",
    "{name}.net",
    "{name}.org",

    # Creative/Short
    "the{name}.com",
    "{name}dc.com",
    "{name}md.com",
    "{name}va.com",
    "{name}scene.com",
    "{name}beat.com",
    "{name}buzz.com",
    "{name}spot.com",
    "{name}corner.com",
    "{name}place.com",

    # Archive/Wiki
    "{name}archive.com",
    "{name}archives.org",
    "{name}wiki.com",
    "{name}wiki.org",

    # Hyper-local
    "{name}neighborhood.com",
    "{name}district.com",
    "{name}area.com",
    "{name}quarter.com",
]


def generate_domains(neighborhood):
    """Generate all domain variations for a neighborhood."""
    domains = set()
    for variant in neighborhood['variants']:
        for pattern in PATTERNS:
            domain = pattern.format(name=variant).lower()
            domains.add(domain)
    return sorted(list(domains))


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


def save_results(neighborhood, domains, available, output_dir):
    """Save results to markdown file."""
    filepath = os.path.join(output_dir, f"{neighborhood['slug']}-domains.md")

    # Score and rank available domains
    def score_domain(d):
        score = 0
        domain = d['domain']
        # Prefer .com
        if domain.endswith('.com'): score += 30
        elif domain.endswith('.org'): score += 20
        elif domain.endswith('.net'): score += 10
        # Prefer shorter
        score -= len(domain) * 0.5
        # Prefer primary variant
        if neighborhood['variants'][0] in domain: score += 15
        # Prefer history-related
        if 'history' in domain: score += 20
        if 'almanac' in domain: score += 18
        if 'chronicle' in domain: score += 15
        if 'heritage' in domain: score += 12
        # Avoid generic terms
        if 'online' in domain: score -= 5
        if 'site' in domain: score -= 5
        return score

    ranked = sorted(available, key=score_domain, reverse=True)

    with open(filepath, 'w') as f:
        f.write(f"# Domain Research: {neighborhood['name']}\n\n")
        f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")

        f.write(f"## Summary\n\n")
        f.write(f"- **Total checked:** {len(domains)}\n")
        f.write(f"- **Available:** {len(available)}\n")
        f.write(f"- **Taken:** {len(domains) - len(available)}\n\n")

        if ranked:
            f.write("## Top Available Domains (Ranked)\n\n")
            f.write("| Rank | Domain | Why |\n")
            f.write("|------|--------|-----|\n")
            for i, d in enumerate(ranked[:25], 1):
                domain = d['domain']
                why = []
                if 'history' in domain: why.append("history keyword")
                if 'almanac' in domain: why.append("almanac brand")
                if 'chronicle' in domain: why.append("chronicle style")
                if domain.endswith('.com'): why.append(".com")
                if len(domain) < 20: why.append("short")
                f.write(f"| {i} | **{domain}** | {', '.join(why) if why else '-'} |\n")
            f.write("\n")

        f.write("## All Available Domains\n\n")
        for d in available:
            f.write(f"- ✅ {d['domain']}\n")
        f.write("\n")

        f.write("<details>\n<summary>All Checked Domains</summary>\n\n")
        f.write("| Domain | Status |\n")
        f.write("|--------|--------|\n")
        for domain in domains:
            avail = any(a['domain'] == domain for a in available)
            status = "✅ Available" if avail else "❌ Taken"
            f.write(f"| {domain} | {status} |\n")
        f.write("\n</details>\n")

    return filepath, ranked


def process_neighborhood(neighborhood, output_dir):
    """Process a single neighborhood."""
    print(f"\n{'='*60}")
    print(f"Processing: {neighborhood['name']}")
    print(f"{'='*60}")

    # Generate domain list
    domains = generate_domains(neighborhood)
    print(f"  Generated {len(domains)} domain variations")

    # Check availability with rate limiting
    available = []
    for i, domain in enumerate(domains):
        result = check_availability(domain)
        if result['available']:
            available.append(result)
            print(f"    ✅ {domain}")
        if (i + 1) % 20 == 0:
            print(f"    Checked {i+1}/{len(domains)}...")
            time.sleep(0.3)  # Rate limiting

    print(f"  Found {len(available)} available domains")

    # Save results
    filepath, ranked = save_results(neighborhood, domains, available, output_dir)
    print(f"  Saved to: {filepath}")

    return {
        'neighborhood': neighborhood['name'],
        'slug': neighborhood['slug'],
        'checked': len(domains),
        'available': len(available),
        'top_domain': ranked[0]['domain'] if ranked else None,
        'top_5': [r['domain'] for r in ranked[:5]] if ranked else []
    }


def main():
    output_dir = '/Users/bb/www/au-park-history/research/domains'
    os.makedirs(output_dir, exist_ok=True)

    # Process specific neighborhood if provided
    if len(sys.argv) > 1:
        slug = sys.argv[1]
        neighborhoods = [n for n in NEIGHBORHOODS if n['slug'] == slug]
        if not neighborhoods:
            print(f"Unknown neighborhood: {slug}")
            print("Available:", [n['slug'] for n in NEIGHBORHOODS])
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
        f.write("| Neighborhood | Top Domain | Available | Top Alternatives |\n")
        f.write("|--------------|------------|-----------|------------------|\n")
        for r in results:
            top5 = ', '.join(r['top_5'][1:4]) if len(r['top_5']) > 1 else '-'
            f.write(f"| {r['neighborhood']} | **{r['top_domain'] or 'None'}** | {r['available']} | {top5} |\n")

        f.write("\n## Recommended Purchases\n\n")
        f.write("Based on availability and ranking:\n\n")
        for r in results:
            if r['top_domain']:
                f.write(f"- **{r['neighborhood']}**: `{r['top_domain']}`\n")

    print(f"\n{'='*60}")
    print(f"COMPLETE! Summary saved to: {summary_path}")
    print(f"{'='*60}")

    # Print quick summary
    print("\nTop domains found:")
    for r in results:
        if r['top_domain']:
            print(f"  {r['neighborhood']}: {r['top_domain']}")


if __name__ == "__main__":
    main()
