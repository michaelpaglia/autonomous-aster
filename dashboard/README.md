# 🌙 AsterDEX Cosmic Trader Dashboard

A beautiful dashboard to track your astrology-based trading bot in real-time!

## Features

- 💰 Real-time balance tracking
- 📊 24-hour PnL chart
- 🎯 Live open positions
- 🌙 Auto-refreshes every 30 seconds
- ✨ Beautiful gradient UI with cosmic vibes

## How It Works

The trading bot (`autonomous_cosmic_trader.py`) exports stats every 10 minutes to `dashboard/public/stats.json` and `dashboard/public/history.json`. This Next.js app reads those files and displays them beautifully.

## Local Development

1. Install dependencies:
```bash
cd dashboard
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Open http://localhost:3000

## Deploy to Vercel

### Option 1: Deploy via Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. From the `dashboard` directory, run:
```bash
vercel
```

3. Follow the prompts to deploy

### Option 2: Deploy via Vercel Website

1. Push your code to GitHub (make sure `dashboard` folder is included)

2. Go to https://vercel.com and sign in

3. Click "Add New Project"

4. Import your GitHub repository

5. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `dashboard`
   - **Build Command**: `npm run build`
   - **Output Directory**: Leave as default

6. Click "Deploy"

## Keeping Data Updated

The bot automatically exports stats every 10 minutes to the `public` folder. To sync this data to your Vercel deployment:

### Method 1: GitHub Actions (Automated)

Add the stats files to git and push regularly:

```bash
# In your main project directory
git add dashboard/public/stats.json dashboard/public/history.json
git commit -m "Update trading stats"
git push
```

Vercel will auto-deploy when you push.

### Method 2: Manual Sync

Use `rsync` or `scp` to copy the stats files to your repo, then push:

```bash
# After bot updates stats
cd /path/to/aster-dex
git add dashboard/public/*.json
git commit -m "Update stats"
git push
```

### Method 3: API Endpoint (Advanced)

For real-time updates without git, you can:
1. Set up a simple server that serves the JSON files
2. Modify the dashboard to fetch from that server instead of local files
3. Use something like a VPS or cloud storage (S3, etc.)

## Notes

- The dashboard shows the last 24 hours of data (144 data points at 10-min intervals)
- Stats refresh every 30 seconds on the dashboard
- The bot must be running for data to update

## Customize

Edit `app/page.tsx` to customize the dashboard appearance and functionality!
