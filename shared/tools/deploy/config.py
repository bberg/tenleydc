"""
Configuration for DMV Neighborhood History Sites Network deployment
16 neighborhood sites covering DC, Maryland, and Virginia
"""

# Site configurations - mapping directory names to domains and metadata
SITES = {
    "tenleytown": {
        "name": "Tenley DC",
        "display_name": "Tenley's Almanac",
        "domain": "tenleydc.com",
        "local_path": "/Users/bb/www/au-park-history/sites/tenleytown",
        "github_repo": "tenleydc",
        "description": "History and community guide for Tenleytown, AU Park, and Upper Northwest DC",
        "region": "DC",
        "neighborhood_full": "Tenleytown"
    },
    "brightwood": {
        "name": "Brightwood DC",
        "display_name": "Brightwood Almanac",
        "domain": "brightwooddc.com",
        "local_path": "/Users/bb/www/au-park-history/sites/brightwood",
        "github_repo": "brightwooddc",
        "description": "History and community guide for Brightwood, Washington DC",
        "region": "DC",
        "neighborhood_full": "Brightwood"
    },
    "kalorama": {
        "name": "Kalorama DC",
        "display_name": "Kalorama Almanac",
        "domain": "kaloramadc.com",
        "local_path": "/Users/bb/www/au-park-history/sites/kalorama",
        "github_repo": "kaloramadc",
        "description": "History and community guide for Kalorama, Washington DC",
        "region": "DC",
        "neighborhood_full": "Kalorama"
    },
    "college-park": {
        "name": "College Park Hub",
        "display_name": "College Park Almanac",
        "domain": "collegeparkhub.com",
        "local_path": "/Users/bb/www/au-park-history/sites/college-park",
        "github_repo": "collegeparkhub",
        "description": "History and community guide for College Park, Maryland",
        "region": "MD",
        "neighborhood_full": "College Park"
    },
    "hyattsville": {
        "name": "Hyattsville Hub",
        "display_name": "Hyattsville Almanac",
        "domain": "hyattsvillehub.com",
        "local_path": "/Users/bb/www/au-park-history/sites/hyattsville",
        "github_repo": "hyattsvillehub",
        "description": "History and community guide for Hyattsville, Maryland",
        "region": "MD",
        "neighborhood_full": "Hyattsville"
    },
    "potomac": {
        "name": "Potomac Spot",
        "display_name": "Potomac Almanac",
        "domain": "potomacspot.com",
        "local_path": "/Users/bb/www/au-park-history/sites/potomac",
        "github_repo": "potomacspot",
        "description": "History and community guide for Potomac, Maryland",
        "region": "MD",
        "neighborhood_full": "Potomac"
    },
    "falls-church": {
        "name": "Falls Church Hub",
        "display_name": "Falls Church Almanac",
        "domain": "fallschurchhub.com",
        "local_path": "/Users/bb/www/au-park-history/sites/falls-church",
        "github_repo": "fallschurchhub",
        "description": "History and community guide for Falls Church, Virginia",
        "region": "VA",
        "neighborhood_full": "Falls Church"
    },
    "vienna": {
        "name": "Vienna Local",
        "display_name": "Vienna Almanac",
        "domain": "viennalocal.com",
        "local_path": "/Users/bb/www/au-park-history/sites/vienna",
        "github_repo": "viennalocal",
        "description": "History and community guide for Vienna, Virginia",
        "region": "VA",
        "neighborhood_full": "Vienna"
    },
    "del-ray": {
        "name": "Del Ray VA",
        "display_name": "Del Ray Almanac",
        "domain": "delrayva.com",
        "local_path": "/Users/bb/www/au-park-history/sites/del-ray",
        "github_repo": "delrayva",
        "description": "History and community guide for Del Ray, Alexandria, Virginia",
        "region": "VA",
        "neighborhood_full": "Del Ray"
    },
    "columbia-heights": {
        "name": "Columbia Heights",
        "display_name": "Columbia Heights Almanac",
        "domain": "cheights.com",
        "local_path": "/Users/bb/www/au-park-history/sites/columbia-heights",
        "github_repo": "cheights",
        "description": "History and community guide for Columbia Heights, Washington DC",
        "region": "DC",
        "neighborhood_full": "Columbia Heights"
    },
    "h-street": {
        "name": "H Street Hub",
        "display_name": "H Street Almanac",
        "domain": "hstreethub.com",
        "local_path": "/Users/bb/www/au-park-history/sites/h-street",
        "github_repo": "hstreethub",
        "description": "History and community guide for H Street Corridor, Washington DC",
        "region": "DC",
        "neighborhood_full": "H Street"
    },
    "sw-waterfront": {
        "name": "SW DC Local",
        "display_name": "SW Waterfront Almanac",
        "domain": "swdclocal.com",
        "local_path": "/Users/bb/www/au-park-history/sites/sw-waterfront",
        "github_repo": "swdclocal",
        "description": "History and community guide for Southwest Waterfront, Washington DC",
        "region": "DC",
        "neighborhood_full": "SW Waterfront"
    },
    "anacostia": {
        "name": "Anacostia Hub",
        "display_name": "Anacostia Almanac",
        "domain": "anacostiahub.com",
        "local_path": "/Users/bb/www/au-park-history/sites/anacostia",
        "github_repo": "anacostiahub",
        "description": "History and community guide for Anacostia, Washington DC",
        "region": "DC",
        "neighborhood_full": "Anacostia"
    },
    "shepherd-park": {
        "name": "Shepherd Park DC",
        "display_name": "Shepherd Park Almanac",
        "domain": "shepherdparkdc.com",
        "local_path": "/Users/bb/www/au-park-history/sites/shepherd-park",
        "github_repo": "shepherdparkdc",
        "description": "History and community guide for Shepherd Park, Washington DC",
        "region": "DC",
        "neighborhood_full": "Shepherd Park"
    },
    "glover-park": {
        "name": "Glover DC",
        "display_name": "Glover Park Almanac",
        "domain": "gloverdc.com",
        "local_path": "/Users/bb/www/au-park-history/sites/glover-park",
        "github_repo": "gloverdc",
        "description": "History and community guide for Glover Park, Washington DC",
        "region": "DC",
        "neighborhood_full": "Glover Park"
    },
    "woodley-park": {
        "name": "Woodley Hub",
        "display_name": "Woodley Park Almanac",
        "domain": "woodleyhub.com",
        "local_path": "/Users/bb/www/au-park-history/sites/woodley-park",
        "github_repo": "woodleyhub",
        "description": "History and community guide for Woodley Park, Washington DC",
        "region": "DC",
        "neighborhood_full": "Woodley Park"
    }
}

# GitHub organization (set to None for personal repos)
GITHUB_ORG = None  # or "dmv-history"

# Network-wide settings
NETWORK_NAME = "DMV Neighborhood History Network"
CONTACT_EMAIL = ""  # Set this before deployment

# All domains for cross-linking and network awareness
ALL_DOMAINS = {
    # DC Sites (10)
    "tenleydc.com": "Tenleytown",
    "brightwooddc.com": "Brightwood",
    "kaloramadc.com": "Kalorama",
    "cheights.com": "Columbia Heights",
    "hstreethub.com": "H Street",
    "swdclocal.com": "SW Waterfront",
    "anacostiahub.com": "Anacostia",
    "shepherdparkdc.com": "Shepherd Park",
    "gloverdc.com": "Glover Park",
    "woodleyhub.com": "Woodley Park",
    # Maryland Sites (3)
    "collegeparkhub.com": "College Park",
    "hyattsvillehub.com": "Hyattsville",
    "potomacspot.com": "Potomac",
    # Virginia Sites (3)
    "fallschurchhub.com": "Falls Church",
    "viennalocal.com": "Vienna",
    "delrayva.com": "Del Ray"
}

# Domain cost tracking
DOMAIN_REGISTRAR = "Cloudflare"
DOMAIN_COST_PER_YEAR = 9.15  # Cloudflare wholesale pricing
TOTAL_DOMAINS = 16
ESTIMATED_ANNUAL_COST = DOMAIN_COST_PER_YEAR * TOTAL_DOMAINS  # ~$146.40

# Sites grouped by region for batch operations
SITES_BY_REGION = {
    "DC": [
        "tenleytown", "brightwood", "kalorama", "columbia-heights",
        "h-street", "sw-waterfront", "anacostia", "shepherd-park",
        "glover-park", "woodley-park"
    ],
    "MD": ["college-park", "hyattsville", "potomac"],
    "VA": ["falls-church", "vienna", "del-ray"]
}

# Domain naming pattern summary
DOMAIN_PATTERNS = {
    "state_suffix": ["tenleydc.com", "brightwooddc.com", "kaloramadc.com",
                     "shepherdparkdc.com", "gloverdc.com", "delrayva.com"],
    "hub_suffix": ["collegeparkhub.com", "hyattsvillehub.com", "fallschurchhub.com",
                   "hstreethub.com", "anacostiahub.com", "woodleyhub.com"],
    "local_suffix": ["viennalocal.com", "swdclocal.com"],
    "spot_suffix": ["potomacspot.com"],
    "short_name": ["cheights.com"]
}
