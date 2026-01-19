# Phase 2: Domain Purchase & DNS Setup

> Register domains and configure DNS to point to your hosting platform.

## Overview

This phase covers:
1. **Domain Registration** - Purchase domains through Cloudflare Registrar
2. **Cloudflare Configuration** - Set up DNS zones and SSL
3. **DNS Records** - Point domains to Railway (or your host)
4. **Verification** - Confirm propagation and SSL

## Prerequisites

Before starting:
- [ ] Final domain selections documented (from Phase 1)
- [ ] Cloudflare account created
- [ ] Payment method added to Cloudflare
- [ ] Railway projects created (will get URLs in Phase 3)

## Step 1: Register Domains on Cloudflare

### Why Cloudflare Registrar?

- At-cost pricing (~$9-12/year for .com)
- Integrated DNS management
- Free SSL/TLS certificates
- DDoS protection included
- No upselling or hidden fees

### Registration Process

1. **Log in to Cloudflare Dashboard**
   - Go to [dash.cloudflare.com](https://dash.cloudflare.com)

2. **Register Domain**
   - Click "Domain Registration" in left sidebar
   - Click "Register Domain"
   - Search for your domain
   - Add to cart and checkout

3. **Repeat for All Domains**
   - Register each domain in your list
   - They'll automatically be added as zones

### Registration Checklist

```markdown
## Domain Registration

| Domain | Registered | Zone Active | Cost |
|--------|------------|-------------|------|
| site1.com | [ ] | [ ] | $10.11 |
| site2.com | [ ] | [ ] | $10.11 |
| ... | [ ] | [ ] | ... |

**Total:** $XX.XX/year
```

## Step 2: Generate Cloudflare API Token

### Create Token for DNS Management

1. Go to [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens)
2. Click "Create Token"
3. Use "Edit zone DNS" template
4. Configure permissions:

```
Zone - DNS - Edit
Zone - Zone - Read
Zone - Zone Settings - Edit
```

5. Set zone resources:
   - Include: All zones (or specific zones)
   - Account: Your account

6. Create and copy the token

### Save Token Securely

Add to your project's `.env` file:

```bash
CLOUDFLARE_TOKEN=your_token_here
```

### Verify Token Works

```bash
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json"
```

Expected response:
```json
{
  "success": true,
  "result": {
    "status": "active"
  }
}
```

## Step 3: Configure DNS Records

### Understanding the Setup

```
User → Cloudflare (DNS + SSL) → Railway (Hosting)
```

DNS records needed per domain:
1. **Root CNAME** (`@`) → Railway app URL
2. **WWW CNAME** → Root domain (for www redirect)

### Option A: Automated Setup (Recommended)

Use the Cloudflare setup script:

```bash
cd shared/tools/deploy

# List zones to verify domains
python cloudflare_setup.py --token $CLOUDFLARE_TOKEN --list-zones

# Set up single domain
python cloudflare_setup.py \
  --token $CLOUDFLARE_TOKEN \
  --domain yourdomain.com \
  --railway-url your-app.up.railway.app

# Dry run first to see changes
python cloudflare_setup.py \
  --token $CLOUDFLARE_TOKEN \
  --domain yourdomain.com \
  --railway-url your-app.up.railway.app \
  --dry-run
```

### Option B: Manual Setup via Dashboard

1. **Go to DNS settings**
   - Select domain in Cloudflare dashboard
   - Click "DNS" in left sidebar

2. **Add Root CNAME Record**
   ```
   Type: CNAME
   Name: @
   Target: your-app.up.railway.app
   Proxy status: Proxied (orange cloud)
   TTL: Auto
   ```

3. **Add WWW CNAME Record**
   ```
   Type: CNAME
   Name: www
   Target: yourdomain.com
   Proxy status: Proxied (orange cloud)
   TTL: Auto
   ```

### Option C: Programmatic Setup

```python
from cloudflare_setup import CloudflareClient, setup_domain_dns

client = CloudflareClient(os.environ["CLOUDFLARE_TOKEN"])

# Verify token
verify = client.verify_token()
print(f"Token status: {verify.get('status')}")

# Set up DNS
result = setup_domain_dns(
    client,
    domain="yourdomain.com",
    railway_url="your-app.up.railway.app"
)

print(f"Setup result: {result}")
```

## Step 4: Configure SSL/TLS

### SSL Settings (Automated by Script)

The Cloudflare script configures these automatically:
- SSL Mode: Full (strict)
- Always Use HTTPS: On
- Minimum TLS Version: 1.2

### Manual SSL Configuration

1. Go to domain in Cloudflare dashboard
2. Click "SSL/TLS" in left sidebar
3. Set "Encryption mode" to **Full (strict)**
4. Go to "Edge Certificates" tab
5. Enable "Always Use HTTPS"
6. Set "Minimum TLS Version" to 1.2

### SSL Modes Explained

| Mode | Description | Use When |
|------|-------------|----------|
| Off | No encryption | Never |
| Flexible | HTTPS to Cloudflare only | Legacy systems |
| Full | End-to-end, any cert | Self-signed certs |
| **Full (strict)** | End-to-end, valid cert | **Railway (recommended)** |

## Step 5: Add Custom Domain in Railway

After DNS is configured, add the domain to Railway:

### Via Railway Dashboard

1. Go to your Railway project
2. Click "Settings" → "Domains"
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `yourdomain.com`)
5. Railway will show verification status

### Via Railway CLI

```bash
railway domain add yourdomain.com
```

### Verification Record (If Needed)

If Railway requires verification, add a TXT record:

```python
from cloudflare_setup import CloudflareClient, add_txt_record

client = CloudflareClient(os.environ["CLOUDFLARE_TOKEN"])

add_txt_record(
    client,
    domain="yourdomain.com",
    name="_railway",
    value="verification-token-from-railway"
)
```

## Step 6: Verify Setup

### Check DNS Propagation

```bash
# Check CNAME record
dig yourdomain.com CNAME +short

# Check A record (after Cloudflare resolves)
dig yourdomain.com A +short

# Full DNS lookup
dig yourdomain.com ANY
```

### Test HTTPS Access

```bash
# Should return 200
curl -I https://yourdomain.com

# Check SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com 2>/dev/null | openssl x509 -noout -dates
```

### Verification Checklist

```markdown
## Verification: yourdomain.com

| Check | Status | Notes |
|-------|--------|-------|
| DNS Propagated | [ ] | dig shows correct IP |
| HTTPS Works | [ ] | curl returns 200 |
| WWW Redirects | [ ] | www → root domain |
| SSL Valid | [ ] | Lock icon in browser |
| Railway Connected | [ ] | Dashboard shows verified |
```

## DNS Records Reference

### Standard Setup (Per Domain)

```
# Root domain CNAME (flattened by Cloudflare)
yourdomain.com.    CNAME   your-app.up.railway.app.

# WWW redirect
www.yourdomain.com.    CNAME   yourdomain.com.
```

## Troubleshooting

### DNS Not Propagating

**Symptoms:** Domain shows old records or not resolving
**Solutions:**
- Wait 5-15 minutes (Cloudflare is fast)
- Clear local DNS cache: `sudo dscacheutil -flushcache`
- Check with external tool: [whatsmydns.net](https://www.whatsmydns.net/)

### SSL Certificate Errors

**Symptoms:** Browser shows "Not Secure" or certificate error
**Solutions:**
- Ensure SSL mode is "Full (strict)" in Cloudflare
- Verify Railway has custom domain added
- Wait for certificate provisioning (up to 24h)
- Check Railway domain status in dashboard

### 521 Error (Web Server Is Down)

**Symptoms:** Cloudflare 521 error page
**Solutions:**
- Verify Railway app is running
- Check Railway deployment logs
- Ensure CNAME points to correct Railway URL

### 525 SSL Handshake Failed

**Symptoms:** Cloudflare 525 error
**Solutions:**
- Change SSL mode to "Full" (not strict)
- Check if Railway is serving HTTPS
- Regenerate Railway domain

## Files Reference

### Project Files

```
shared/tools/deploy/
├── cloudflare_setup.py    # Main DNS automation script
├── dns_records.json       # Record configurations
└── config.py              # Domain mappings
```

### Environment Variables

```bash
# .env file
CLOUDFLARE_TOKEN=your_cf_token_here
```

## Output Checklist

After completing this phase:

- [ ] All domains registered on Cloudflare
- [ ] Cloudflare API token created and saved
- [ ] DNS records configured for all domains
- [ ] SSL/TLS set to Full (strict) mode
- [ ] Custom domains added in Railway
- [ ] All domains verified and accessible via HTTPS
- [ ] WWW subdomains redirecting properly

---

**Next Step:** [03-DEPLOYMENT-INFRASTRUCTURE.md](./03-DEPLOYMENT-INFRASTRUCTURE.md)
