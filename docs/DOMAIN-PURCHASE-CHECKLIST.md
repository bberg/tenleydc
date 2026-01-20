# Domain Purchase Checklist - 16 Neighborhood Sites

**Status:** Ready for Purchase
**Registrar:** Cloudflare ($9.15/domain)
**Total Cost:** ~$146.40/year

---

## Quick Reference Table

| # | Domain | Neighborhood | Region | Status |
|---|--------|--------------|--------|--------|
| 1 | tenleydc.com | Tenleytown | DC | [ ] |
| 2 | brightwooddc.com | Brightwood | DC | [ ] |
| 3 | kaloramadc.com | Kalorama | DC | [ ] |
| 4 | collegeparkhub.com | College Park | MD | [ ] |
| 5 | hyattsvillehub.com | Hyattsville | MD | [ ] |
| 6 | potomacspot.com | Potomac | MD | [ ] |
| 7 | fallschurchhub.com | Falls Church | VA | [ ] |
| 8 | viennalocal.com | Vienna | VA | [ ] |
| 9 | delrayva.com | Del Ray | VA | [ ] |
| 10 | cheights.com | Columbia Heights | DC | [ ] |
| 11 | hstreethub.com | H Street | DC | [ ] |
| 12 | swdclocal.com | SW Waterfront | DC | [ ] |
| 13 | anacostiahub.com | Anacostia | DC | [ ] |
| 14 | shepherdparkdc.com | Shepherd Park | DC | [ ] |
| 15 | gloverdc.com | Glover Park | DC | [ ] |
| 16 | woodleyhub.com | Woodley Park | DC | [ ] |

---

## Purchase Order (By Region)

### DC Sites (10 domains)

```
tenleydc.com
brightwooddc.com
kaloramadc.com
cheights.com
hstreethub.com
swdclocal.com
anacostiahub.com
shepherdparkdc.com
gloverdc.com
woodleyhub.com
```

### Maryland Sites (3 domains)

```
collegeparkhub.com
hyattsvillehub.com
potomacspot.com
```

### Virginia Sites (3 domains)

```
fallschurchhub.com
viennalocal.com
delrayva.com
```

---

## Domain Naming Pattern Summary

| Pattern | Count | Examples |
|---------|-------|----------|
| State suffix (dc/va) | 6 | tenleydc.com, brightwooddc.com, delrayva.com |
| Hub suffix | 6 | collegeparkhub.com, hstreethub.com, anacostiahub.com |
| Local suffix | 2 | viennalocal.com, swdclocal.com |
| Spot suffix | 1 | potomacspot.com |
| Short name | 1 | cheights.com |

---

## Post-Purchase Setup

After purchasing each domain, complete these steps:

### 1. DNS Configuration (Cloudflare)
- [ ] Set up CNAME record pointing to Railway
- [ ] Enable HTTPS/SSL
- [ ] Configure email forwarding if needed

### 2. Railway Deployment
- [ ] Create Railway project for site
- [ ] Link GitHub repository
- [ ] Configure custom domain

### 3. Analytics & SEO
- [ ] Create GA4 property
- [ ] Add tracking code to site
- [ ] Submit to Google Search Console
- [ ] Generate and submit sitemap

---

## Cloudflare Registrar Steps

1. Log into Cloudflare Dashboard
2. Navigate to "Registrar" > "Register Domains"
3. Search for domain
4. Add to cart
5. Complete purchase
6. Enable auto-renewal

### Cloudflare DNS Setup (per domain)

1. Go to domain in Cloudflare
2. Navigate to DNS > Records
3. Add CNAME record:
   - Type: CNAME
   - Name: @
   - Target: [railway-app-url].railway.app
   - Proxy: Enabled (orange cloud)
4. Add www redirect:
   - Type: CNAME
   - Name: www
   - Target: [railway-app-url].railway.app
   - Proxy: Enabled

---

## Verification Commands

After setup, verify each domain:

```bash
# Check DNS propagation
dig +short tenleydc.com

# Check HTTPS
curl -I https://tenleydc.com

# Check redirect from www
curl -I https://www.tenleydc.com
```

---

## Cost Breakdown

| Item | Cost |
|------|------|
| 16 domains @ $9.15/year | $146.40 |
| Railway hosting (~$5/site/month) | $960/year |
| **Total annual cost** | ~$1,106/year |

---

## Notes

- All domains verified available as of domain research date
- Purchase all at once to lock in availability
- Set auto-renewal to prevent expiration
- Keep registration info consistent across all domains
