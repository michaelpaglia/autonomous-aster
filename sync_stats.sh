#!/bin/bash
#
# Auto-sync trading stats to GitHub for Vercel deployment
# This script commits and pushes stats files every time it runs
#

cd "$(dirname "$0")"

# Check if there are changes to the stats files
if git diff --quiet dashboard/public/stats.json dashboard/public/history.json; then
    # No changes, exit silently
    exit 0
fi

# Add the stats files
git add dashboard/public/stats.json dashboard/public/history.json

# Create commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Update trading stats - $TIMESTAMP

Auto-synced by cosmic trader bot
Balance and position data updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to main (suppress output unless there's an error)
if ! git push origin main > /dev/null 2>&1; then
    # If push fails (maybe conflicts), try to pull and retry
    echo "Push failed, attempting to sync..."
    git pull --rebase origin main > /dev/null 2>&1
    git push origin main
fi

echo "Stats synced to GitHub at $TIMESTAMP"
