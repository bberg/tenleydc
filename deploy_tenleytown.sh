#!/bin/bash
# Deploy Tenleytown to Railway + Cloudflare
# Run after purchasing tenleydc.com on Cloudflare

set -e

# Load environment variables
source .env

DOMAIN="tenleydc.com"
PROJECT_NAME="tenleydc"

echo "=== Deploying $DOMAIN ==="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (if needed)
echo ""
echo "Step 1: Railway Setup"
echo "====================="
railway login --browserless 2>/dev/null || true

# Create new project or link existing
echo "Creating Railway project: $PROJECT_NAME"
railway init --name $PROJECT_NAME 2>/dev/null || echo "Project may already exist"

# Deploy
echo "Deploying to Railway..."
railway up --detach

# Get the Railway domain
echo ""
echo "Getting Railway deployment URL..."
RAILWAY_URL=$(railway domain 2>/dev/null || echo "Check Railway dashboard for URL")
echo "Railway URL: $RAILWAY_URL"

# Cloudflare DNS setup
echo ""
echo "Step 2: Cloudflare DNS"
echo "======================"
echo "Setting up DNS records for $DOMAIN..."

# Get zone ID for the domain
ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN" \
    -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
    -H "Content-Type: application/json" | python3 -c "import sys, json; print(json.load(sys.stdin)['result'][0]['id'])" 2>/dev/null)

if [ -z "$ZONE_ID" ]; then
    echo "ERROR: Could not find Cloudflare zone for $DOMAIN"
    echo "Make sure the domain is added to your Cloudflare account"
    exit 1
fi

echo "Zone ID: $ZONE_ID"

# Note: You'll need to add the Railway custom domain first, then get the target
echo ""
echo "=== MANUAL STEPS REQUIRED ==="
echo ""
echo "1. Go to Railway dashboard: https://railway.app/dashboard"
echo "2. Open your project, go to Settings → Networking → Custom Domains"
echo "3. Add: $DOMAIN"
echo "4. Add: www.$DOMAIN"
echo "5. Copy the CNAME target (e.g., xxx.up.railway.app)"
echo ""
echo "Then run this to add DNS records:"
echo ""
echo "  RAILWAY_TARGET='your-railway-url.up.railway.app'"
echo ""
echo "  # Add root CNAME"
echo "  curl -X POST 'https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records' \\"
echo "    -H 'Authorization: Bearer $CLOUDFLARE_TOKEN' \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    --data '{\"type\":\"CNAME\",\"name\":\"@\",\"content\":\"'\$RAILWAY_TARGET'\",\"proxied\":true}'"
echo ""
echo "  # Add www CNAME"
echo "  curl -X POST 'https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records' \\"
echo "    -H 'Authorization: Bearer $CLOUDFLARE_TOKEN' \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    --data '{\"type\":\"CNAME\",\"name\":\"www\",\"content\":\"'\$RAILWAY_TARGET'\",\"proxied\":true}'"
echo ""
echo "=== DONE ==="
