# 🚀 Vercel Dashboard Setup

## The Issue

The trading bot runs **locally** on your machine and exports stats to `dashboard/public/stats.json`, but Vercel hosts a **static site** that doesn't automatically sync with your local files.

This means: **Vercel will show placeholder data until you update it.**

## Solutions

### Option 1: Run Dashboard Locally (Easiest)

Run the dashboard on your local machine alongside the bot:

```bash
# Terminal 1: Run the bot
python autonomous_cosmic_trader.py

# Terminal 2: Run the dashboard
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000 - it will show **live data** as the bot updates the JSON files every 10 minutes!

**Pros**: Real-time updates, no deployment needed
**Cons**: Only accessible on your machine

---

### Option 2: Manual Sync to Vercel

After the bot runs and updates stats, commit and push:

```bash
# After bot has run for a while
git add dashboard/public/*.json
git commit -m "Update trading stats"
git push
```

Vercel will auto-deploy with the new data.

**Pros**: Simple, uses Vercel
**Cons**: Manual process, not real-time

---

### Option 3: Automated GitHub Actions (Advanced)

Create `.github/workflows/update-stats.yml`:

```yaml
name: Update Stats
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run bot and export stats
        run: |
          python -m pip install -r requirements.txt
          python stats_exporter.py  # Just export, don't trade
      - name: Commit stats
        run: |
          git config user.name "Bot"
          git config user.email "bot@bot.com"
          git add dashboard/public/*.json
          git commit -m "Update stats" || exit 0
          git push
```

**Pros**: Fully automated
**Cons**: Complex setup, GitHub Actions costs

---

### Option 4: Use Cloud Storage (Best for Production)

Host the JSON files on AWS S3, Cloudflare R2, or similar:

1. **Modify bot to upload to S3**:
```python
# In stats_exporter.py
import boto3
s3 = boto3.client('s3')
s3.put_object(Bucket='my-bucket', Key='stats.json', Body=json.dumps(stats))
```

2. **Update dashboard to fetch from S3**:
```typescript
// In dashboard/app/page.tsx
fetch('https://my-bucket.s3.amazonaws.com/stats.json')
```

3. **Enable CORS on your bucket**

**Pros**: Real-time updates, scalable, proper production setup
**Cons**: Requires cloud setup, small hosting costs (~$0.01/month)

---

## Current State

The dashboard on Vercel will show:
- **Placeholder data** (0 balance, no positions)
- Updates only when you push new JSON files to git

## Recommended Setup

For development/personal use:
→ **Option 1** (run locally alongside bot)

For showing others/public access:
→ **Option 2** (manual sync) or **Option 4** (cloud storage)

For automated/production:
→ **Option 4** (cloud storage)

---

## Quick Start: Local Dashboard

```bash
cd dashboard
npm install
npm run dev
```

While the bot runs in another terminal:
```bash
python autonomous_cosmic_trader.py
```

The dashboard will auto-refresh every 30 seconds and show live data! 🌙✨
