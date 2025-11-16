# 🪟 Windows Auto-Sync Setup for Vercel Dashboard

Since you're on Windows Server, we'll use **Task Scheduler** instead of cron.

## 📋 Setup Instructions

### Step 1: Create the Batch Script

First, let's create a Windows batch file version of the sync script.

Create `sync_stats.bat` in your `aster-dex` folder:

```batch
@echo off
cd /d "%~dp0"

REM Check if there are changes to stats files
git diff --quiet dashboard\public\stats.json dashboard\public\history.json
if %errorlevel% equ 0 (
    REM No changes, exit silently
    exit /b 0
)

REM Add the stats files
git add dashboard\public\stats.json dashboard\public\history.json

REM Create commit with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/: " %%a in ('time /t') do (set mytime=%%a:%%b:00)
set timestamp=%mydate% %mytime%

git commit -m "Update trading stats - %timestamp%

Auto-synced by cosmic trader bot
Balance and position data updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

REM Push to main
git push origin main >nul 2>&1
if %errorlevel% neq 0 (
    echo Push failed, attempting to sync...
    git pull --rebase origin main >nul 2>&1
    git push origin main
)

echo Stats synced to GitHub at %timestamp%
```

Save this as `sync_stats.bat` in your `C:\path\to\aster-dex\` folder.

---

### Step 2: Test the Batch Script

```cmd
cd C:\path\to\aster-dex
sync_stats.bat
```

You should see: `Stats synced to GitHub at 2025-11-15 20:10:00`

---

### Step 3: Set Up Task Scheduler

#### Option A: Using GUI (Easiest)

1. **Open Task Scheduler**:
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**:
   - Click "Create Basic Task" in the right panel
   - Name: `Cosmic Stats Sync`
   - Description: `Auto-sync trading stats to GitHub every 10 minutes`
   - Click Next

3. **Set Trigger**:
   - Select "Daily"
   - Click Next
   - Start date: Today
   - Recur every: 1 day
   - Click Next

4. **Set Action**:
   - Select "Start a program"
   - Click Next
   - Program/script: `C:\path\to\aster-dex\sync_stats.bat`
   - Start in: `C:\path\to\aster-dex`
   - Click Next

5. **Finish**:
   - Check "Open the Properties dialog"
   - Click Finish

6. **Configure for 10-minute intervals**:
   - In Properties dialog → Triggers tab
   - Double-click your trigger
   - Check "Repeat task every:"
   - Select `10 minutes`
   - For a duration of: `Indefinitely`
   - Click OK

7. **Set to run whether user is logged on or not**:
   - General tab
   - Select "Run whether user is logged on or not"
   - Check "Run with highest privileges"
   - Click OK
   - Enter your Windows password when prompted

---

#### Option B: Using Command Line (Advanced)

```cmd
schtasks /create /tn "Cosmic Stats Sync" /tr "C:\path\to\aster-dex\sync_stats.bat" /sc minute /mo 10 /st 00:00 /ru SYSTEM
```

Replace `C:\path\to\aster-dex` with your actual path!

---

### Step 4: Verify Task is Running

```cmd
REM List all scheduled tasks
schtasks /query /tn "Cosmic Stats Sync"

REM Or view in Task Scheduler GUI
taskschd.msc
```

---

### Step 5: Monitor Sync Activity

Create a log file by modifying the batch script to redirect output:

```batch
REM Add to the end of sync_stats.bat:
>> sync_stats.log 2>&1
```

Then view the log:
```cmd
type sync_stats.log
```

Or monitor in real-time with PowerShell:
```powershell
Get-Content sync_stats.log -Wait -Tail 10
```

---

## 🔍 Troubleshooting

### Task Not Running?

Check Task Scheduler status:
```cmd
schtasks /query /tn "Cosmic Stats Sync" /v /fo list
```

### Check Task History

1. Open Task Scheduler (`taskschd.msc`)
2. Find "Cosmic Stats Sync" in the task list
3. Click on "History" tab at the bottom
4. Look for success/error messages

### Git Push Failing?

Make sure Git credentials are cached:
```cmd
git config --global credential.helper wincred
```

Test GitHub connection:
```cmd
ssh -T git@github.com
```

### Path Issues?

Use full paths everywhere in the batch script:
```batch
"C:\Program Files\Git\bin\git.exe" add dashboard\public\*.json
```

Find git.exe location:
```cmd
where git
```

---

## 🎯 Expected Behavior

Once set up:

1. **Bot runs** every 10 minutes
2. **Exports stats** to `dashboard\public\stats.json`
3. **Task Scheduler runs** every 10 minutes
4. **Batch script commits** changes (only if files changed)
5. **Pushes to GitHub**
6. **Vercel detects** the commit
7. **Auto-deploys** new version (~30 seconds)
8. **Dashboard updates** with fresh data!

---

## 🛑 Stop Auto-Sync

To disable:

**GUI Method**:
1. Open Task Scheduler (`taskschd.msc`)
2. Find "Cosmic Stats Sync"
3. Right-click → Disable

**Command Line**:
```cmd
schtasks /end /tn "Cosmic Stats Sync"
schtasks /delete /tn "Cosmic Stats Sync" /f
```

---

## 📊 Quick Test

```cmd
REM 1. Navigate to project
cd C:\path\to\aster-dex

REM 2. Test the batch script
sync_stats.bat

REM 3. Check if it committed
git log -1

REM 4. Manually trigger the scheduled task
schtasks /run /tn "Cosmic Stats Sync"

REM 5. Check last run time
schtasks /query /tn "Cosmic Stats Sync"
```

---

## ✅ Quick Setup Checklist

- [ ] Created `sync_stats.bat` script
- [ ] Tested script manually (`sync_stats.bat`)
- [ ] Opened Task Scheduler (`taskschd.msc`)
- [ ] Created task with 10-minute interval
- [ ] Set to run with highest privileges
- [ ] Verified task is enabled
- [ ] Checked task history for successful runs
- [ ] Verified commits on GitHub
- [ ] Verified Vercel is deploying
- [ ] Checked dashboard shows new data

---

## 🚀 Alternative: PowerShell Script (Optional)

If you prefer PowerShell, here's a more robust version:

Create `sync_stats.ps1`:

```powershell
Set-Location $PSScriptRoot

# Check for changes
$changes = git diff --quiet dashboard/public/stats.json dashboard/public/history.json
if ($LASTEXITCODE -eq 0) {
    exit 0
}

# Add files
git add dashboard/public/stats.json dashboard/public/history.json

# Create commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = @"
Update trading stats - $timestamp

Auto-synced by cosmic trader bot
Balance and position data updated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"@

git commit -m $commitMsg

# Push with error handling
$pushResult = git push origin main 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Push failed, attempting to sync..."
    git pull --rebase origin main
    git push origin main
}

Write-Host "Stats synced to GitHub at $timestamp"
```

Then in Task Scheduler, use:
- Program: `powershell.exe`
- Arguments: `-ExecutionPolicy Bypass -File "C:\path\to\aster-dex\sync_stats.ps1"`

---

## 🌙 You're All Set!

Your Vercel dashboard will now auto-update every 10 minutes with the latest trading data!

May the cosmic sync be with you on Windows! 🪟✨
