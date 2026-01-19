# Phase 5: Analytics & Monitoring

> Set up Google Analytics 4, Search Console, and custom monitoring for your site network.

## Overview

This phase covers:
1. **Google Analytics 4** - Traffic tracking and user behavior
2. **Google Search Console** - SEO performance and indexing
3. **Custom Site Monitor** - Uptime, performance, and alert system
4. **Tracking Code Injection** - Automating analytics deployment

## Prerequisites

Before starting:
- [ ] All sites deployed and accessible (Phase 3)
- [ ] Google Cloud service account created
- [ ] APIs enabled in Google Cloud:
  - Google Analytics Admin API
  - Google Analytics Data API
  - Search Console API

## Part 1: Google Analytics 4 Setup

### Step 1: Prepare Google Cloud

1. **Create Service Account**
   ```
   Go to: IAM & Admin → Service Accounts
   Create account with Analytics Admin role
   Download JSON key file
   ```

2. **Enable Required APIs**
   ```bash
   # Using gcloud CLI
   gcloud services enable analyticsadmin.googleapis.com
   gcloud services enable analyticsdata.googleapis.com
   gcloud services enable searchconsole.googleapis.com
   ```

3. **Grant Access to GA Account**
   - Go to GA Admin → Account Access Management
   - Add service account email as Administrator

### Step 2: Create GA4 Properties

#### Option A: Automated Setup

```bash
cd shared/tools/deploy

# List accessible accounts
python google_analytics_setup.py \
  --credentials /path/to/service-account.json \
  --list-accounts

# List existing properties
python google_analytics_setup.py \
  --credentials /path/to/service-account.json \
  --account-id YOUR_ACCOUNT_ID \
  --list-properties

# Dry run - see what would be created
python google_analytics_setup.py \
  --credentials /path/to/service-account.json \
  --account-id YOUR_ACCOUNT_ID \
  --dry-run

# Create properties for all sites
python google_analytics_setup.py \
  --credentials /path/to/service-account.json \
  --account-id YOUR_ACCOUNT_ID
```

Output file: `ga_measurement_ids.json`
```json
{
  "site-1": "G-XXXXXXXXXX",
  "site-2": "G-YYYYYYYYYY",
  "site-3": "G-ZZZZZZZZZZ"
}
```

#### Option B: Manual Setup

1. Go to [Google Analytics](https://analytics.google.com/)
2. Admin → Create Property
3. Enter property name (site name)
4. Select time zone and currency
5. Create Web Data Stream
6. Enter website URL
7. Copy Measurement ID (G-XXXXXXXX)

### Step 3: Inject Tracking Code

#### Automated Injection

```bash
# Dry run first
python inject_analytics.py \
  --measurement-ids ga_measurement_ids.json \
  --dry-run

# Inject into all sites
python inject_analytics.py \
  --measurement-ids ga_measurement_ids.json

# Inject into single site
python inject_analytics.py \
  --measurement-ids ga_measurement_ids.json \
  --site site-1
```

#### Manual Injection

Add to `<head>` section of your HTML templates:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Step 4: Custom Event Tracking

Add custom events for site-specific tracking:

```javascript
// Track user interactions
function trackEvent(action, label, value) {
  gtag('event', action, {
    'event_category': 'User Interaction',
    'event_label': label,
    'value': value || 1
  });
}

// Examples:
trackEvent('button_click', 'signup');
trackEvent('form_submit', 'contact');
trackEvent('page_scroll', 'bottom', 100);

// Track session duration
var sessionStart = Date.now();
window.addEventListener('beforeunload', function() {
  var duration = Math.round((Date.now() - sessionStart) / 1000);
  gtag('event', 'session_duration', {
    'event_category': 'Engagement',
    'value': duration
  });
});
```

### Step 5: Verify Tracking

1. **Real-time Reports**
   - Go to GA → Reports → Realtime
   - Visit your site in another browser
   - Should see activity within seconds

2. **Debug View**
   - Install [GA Debugger extension](https://chrome.google.com/webstore/detail/google-analytics-debugger)
   - Check browser console for gtag calls

3. **Tag Assistant**
   - Visit [Tag Assistant](https://tagassistant.google.com/)
   - Enter your site URL
   - Verify tag is firing correctly

## Part 2: Google Search Console Setup

### Step 1: Add Sites to Search Console

#### Automated Setup

```bash
python search_console_setup.py \
  --credentials /path/to/service-account.json \
  --dry-run

python search_console_setup.py \
  --credentials /path/to/service-account.json
```

#### Manual Setup

1. Go to [Search Console](https://search.google.com/search-console)
2. Click "Add Property"
3. Choose "URL prefix" method
4. Enter: `https://yourdomain.com`

### Step 2: Verify Ownership

#### DNS Verification (Recommended)

Add TXT record to your domain:
```
Type: TXT
Name: @
Value: google-site-verification=XXXXXXXXXXXXX
```

Using Cloudflare script:
```python
from cloudflare_setup import CloudflareClient, add_txt_record

client = CloudflareClient(os.environ["CLOUDFLARE_TOKEN"])
add_txt_record(
    client,
    domain="yourdomain.com",
    name="@",
    value="google-site-verification=XXXXXXXXXXXXX"
)
```

### Step 3: Submit Sitemaps

1. Go to Search Console → Sitemaps
2. Enter: `sitemap.xml`
3. Click Submit

### Step 4: Monitor Search Performance

Key metrics to track:
- **Impressions** - How often your site appears in search
- **Clicks** - How often users click through
- **CTR** - Click-through rate
- **Position** - Average ranking position

## Part 3: Custom Site Monitoring

### Monitoring Agent Architecture

```
site-monitor/
├── main.py              # Entry point
├── config/
│   └── settings.py      # Configuration
├── monitors/
│   ├── uptime.py        # Availability checks
│   ├── analytics.py     # GA4 data fetching
│   └── search.py        # Search Console data
├── notifications/
│   ├── email.py         # Email alerts (Resend)
│   └── push.py          # Push notifications (Pushover)
├── scheduler/
│   └── jobs.py          # Scheduled tasks
└── requirements.txt
```

### Configuration

```python
# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Sites to monitor
    properties: list = [
        {"name": "Site 1", "url": "https://site1.com", "ga_property": "properties/123"},
        {"name": "Site 2", "url": "https://site2.com", "ga_property": "properties/124"},
    ]

    # Alert thresholds
    response_time_warning_ms: int = 2000
    response_time_critical_ms: int = 5000
    traffic_drop_warning_pct: int = 20
    traffic_drop_critical_pct: int = 50
    ssl_expiry_warning_days: int = 30

    # Notification settings
    resend_api_key: str = ""
    pushover_app_token: str = ""
    pushover_user_key: str = ""
    notification_email: str = ""

    # Google APIs
    google_service_account_json: str = ""

    # Server
    port: int = 8080
```

### Monitoring Checks

#### Uptime Check (Every 5 Minutes)

```python
async def check_uptime(url: str) -> dict:
    """Check if a site is up and responsive."""
    start = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                response_time = (time.time() - start) * 1000
                return {
                    "status": "up",
                    "status_code": response.status,
                    "response_time_ms": response_time,
                }
    except Exception as e:
        return {
            "status": "down",
            "error": str(e),
        }
```

#### SSL Certificate Check

```python
def check_ssl_expiry(domain: str) -> dict:
    """Check SSL certificate expiration."""
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_remaining = (expiry - datetime.now()).days

            return {
                "domain": domain,
                "expires": expiry.isoformat(),
                "days_remaining": days_remaining,
                "status": "ok" if days_remaining > 30 else "warning",
            }
```

### Alert System

#### Email Alerts (Resend)

```python
import resend

def send_email_alert(subject: str, body: str, to: str):
    """Send email alert via Resend."""
    resend.api_key = settings.resend_api_key

    resend.Emails.send({
        "from": "monitor@yourdomain.com",
        "to": to,
        "subject": f"[Site Monitor] {subject}",
        "html": body,
    })
```

#### Push Notifications (Pushover)

```python
import httpx

def send_push_alert(title: str, message: str, priority: int = 0):
    """Send push notification via Pushover."""
    httpx.post("https://api.pushover.net/1/messages.json", data={
        "token": settings.pushover_app_token,
        "user": settings.pushover_user_key,
        "title": title,
        "message": message,
        "priority": priority,
    })
```

### Running the Monitor

```bash
cd site-monitor

# Run all checks once
python main.py --check

# Run uptime check only
python main.py --uptime

# Start scheduler (production)
python main.py
```

### Deploy Monitor to Railway

```toml
# railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python main.py"
```

Environment variables needed:
```
RESEND_API_KEY=re_xxx
PUSHOVER_APP_TOKEN=xxx
PUSHOVER_USER_KEY=xxx
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
NOTIFICATION_EMAIL=you@email.com
```

## Verification Checklist

After completing this phase:

- [ ] GA4 properties created for all sites
- [ ] Measurement IDs documented
- [ ] Tracking code injected into all templates
- [ ] Real-time data showing in GA4
- [ ] Sites added to Search Console
- [ ] DNS verification complete
- [ ] Sitemaps submitted
- [ ] Monitoring agent deployed (optional)
- [ ] Email alerts configured (optional)
- [ ] Push notifications configured (optional)
- [ ] SSL expiry monitoring active

## Files Reference

### Analytics Scripts

| File | Purpose |
|------|---------|
| `google_analytics_setup.py` | Create GA4 properties |
| `search_console_setup.py` | Set up Search Console |
| `inject_analytics.py` | Inject tracking code |
| `ga_measurement_ids.json` | Store measurement IDs |

### Monitoring Agent

| File | Purpose |
|------|---------|
| `site-monitor/main.py` | Entry point |
| `site-monitor/config/settings.py` | Configuration |
| `site-monitor/monitors/uptime.py` | Availability checks |
| `site-monitor/notifications/email.py` | Email alerts |

## Troubleshooting

### Analytics Not Tracking

1. Check measurement ID is correct
2. Verify script is in `<head>` section
3. Check for JavaScript errors in console
4. Ensure no ad blockers are active
5. Try GA Debugger extension

### Search Console Not Verifying

1. Check DNS TXT record is correct
2. Wait for DNS propagation (5-10 min)
3. Try HTML file verification method
4. Ensure service account has access

### Monitor Alerts Not Sending

1. Verify API keys are correct
2. Check notification email is valid
3. Test notification endpoints manually
4. Check monitor logs for errors

---

**Next Step:** [06-SEO-IMPLEMENTATION.md](./06-SEO-IMPLEMENTATION.md)
