# 🔄 Auto-Sync Setup for Vercel Dashboard

This guide sets up automatic syncing of trading stats to GitHub, which triggers Vercel to redeploy with fresh data.

## How It Works

```
Bot runs → Exports stats.json → Cron job commits → GitHub updates → Vercel deploys
   (every 10 min)     ↓              ↓                  ↓              ↓
                Local files    Git commit          Auto-trigger    Live dashboard
```

---

## 📋 Setup Instructions

### Step 1: Test the Sync Script

First, make sure the script works:

```bash
cd ~/aster-dex  # Or wherever your repo is

# Test the script
./sync_stats.sh

# You should see:
# "Stats synced to GitHub at 2025-11-15 19:45:00"
```

If you see an error about permissions:
```bash
chmod +x sync_stats.sh
```

---

### Step 2: Set Up Cron Job

**Option A: Run Every 10 Minutes** (matches bot interval)

```bash
# Edit crontab
crontab -e

# Add this line (press 'i' to insert, then paste):
*/10 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1

# Save and exit:
# Press ESC, then type :wq and press ENTER
```

**Replace `/path/to/aster-dex`** with your actual path!

To find it:
```bash
cd ~/aster-dex
pwd  # Copy this path
```

---

**Option B: Run Every 15 Minutes** (less frequent)

```bash
crontab -e

# Add:
*/15 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1
```

---

**Option C: Run Every 30 Minutes** (minimum overhead)

```bash
crontab -e

# Add:
*/30 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1
```

---

### Step 3: Verify Cron Job is Active

```bash
# List current cron jobs
crontab -l

# You should see your new job listed
```

---

### Step 4: Monitor Sync Activity

```bash
# Watch the sync log
tail -f sync_stats.log

# You'll see entries like:
# Stats synced to GitHub at 2025-11-15 19:50:00
# Stats synced to GitHub at 2025-11-15 20:00:00
```

---

## 🔍 Troubleshooting

### Cron Job Not Running?

Check cron service is running:
```bash
# On Linux
sudo service cron status

# On Mac
sudo launchctl list | grep cron
```

### Check Cron Logs

```bash
# On Linux
grep CRON /var/log/syslog | tail -20

# On Mac
log show --predicate 'eventMessage contains "cron"' --last 1h
```

### Git Push Failing?

Make sure SSH keys are set up:
```bash
# Test GitHub connection
ssh -T git@github.com

# Should say: "Hi username! You've successfully authenticated..."
```

If using HTTPS instead of SSH:
```bash
# Check remote URL
git remote -v

# If it shows HTTPS, you may need to cache credentials
git config --global credential.helper cache
```

### Script Not Finding Git?

Add full path to git in script:
```bash
# Find git path
which git

# Edit sync_stats.sh and use full path like:
/usr/bin/git add dashboard/public/*.json
```

---

## 🎯 Expected Behavior

Once set up:

1. **Bot runs** every 10 minutes
2. **Exports stats** to `dashboard/public/stats.json`
3. **Cron job runs** every 10-30 minutes
4. **Commits changes** to git (only if files changed)
5. **Pushes to GitHub**
6. **Vercel detects** the commit
7. **Auto-deploys** new version (~30 seconds)
8. **Dashboard updates** with fresh data!

---

## ⏱️ Timeline Example

```
7:00 PM - Bot cycle runs, updates stats
7:10 PM - Cron syncs to GitHub
7:10 PM - Vercel starts deploying
7:11 PM - Vercel dashboard live with 7:00 PM data

7:10 PM - Bot cycle runs, updates stats
7:20 PM - Cron syncs to GitHub
7:20 PM - Vercel starts deploying
7:21 PM - Vercel dashboard live with 7:10 PM data
```

**Dashboard lag**: 10-20 minutes behind live data (acceptable!)

---

## 📊 Verify It's Working

1. **Check GitHub**: Go to your repo on GitHub.com
   - Should see commits like "Update trading stats - 2025-11-15 19:50:00"
   - Every 10-30 minutes

2. **Check Vercel**: Go to vercel.com/dashboard
   - Should see auto-deployments triggered by commits
   - Click on deployment to see build logs

3. **Check Dashboard**: Open your Vercel dashboard URL
   - Should see updated balance/positions
   - Timestamp should be recent (within last 10-30 min)

---

## 🛑 Stop Auto-Sync

To disable:
```bash
# Edit crontab
crontab -e

# Delete or comment out the line (add # at start):
# */10 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1

# Save and exit
```

Or remove all cron jobs:
```bash
crontab -r
```

---

## 🎛️ Advanced: Custom Schedule

Cron syntax: `minute hour day month weekday command`

Examples:
```bash
# Every hour at :05 past the hour
5 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1

# Every 5 minutes
*/5 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1

# Only during trading hours (9 AM - 5 PM)
*/10 9-17 * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1

# Every hour on the hour
0 * * * * cd /path/to/aster-dex && ./sync_stats.sh >> sync_stats.log 2>&1
```

Use [crontab.guru](https://crontab.guru) to build custom schedules!

---

## ✅ Quick Setup Checklist

- [ ] Script is executable (`chmod +x sync_stats.sh`)
- [ ] Tested script manually (`./sync_stats.sh`)
- [ ] Cron job added (`crontab -e`)
- [ ] Path is correct in cron job
- [ ] Verified cron job is listed (`crontab -l`)
- [ ] Checked logs after 10 minutes (`tail sync_stats.log`)
- [ ] Verified commits on GitHub
- [ ] Verified Vercel is deploying
- [ ] Checked dashboard shows new data

---

## 🚀 You're All Set!

Your Vercel dashboard will now auto-update every 10-30 minutes with the latest trading data!

May the cosmic sync be with you! 🌙✨
