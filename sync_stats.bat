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
