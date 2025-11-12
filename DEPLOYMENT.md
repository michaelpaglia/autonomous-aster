# 🚀 Server Deployment Guide

## Quick Deploy to Your Server

### 1. On Your Server

```bash
# Clone the repo
git clone <your-github-repo-url>
cd aster-dex

# Run automated setup
chmod +x setup_server.sh
./setup_server.sh
```

The setup script will:
- Install Python 3.11 and dependencies
- Create a virtual environment
- Install all required packages
- Optionally set up systemd service for auto-start

### 2. Verify Configuration

Make sure `config.py` has your credentials (should already be there from GitHub):

```python
# Check these are set correctly:
ASTERDEX_MAIN_WALLET = "0xb1f964b5ccf4601979bda5300077e0b71cb68d76"
ASTERDEX_API_WALLET = "0xB8c850956834E9A3965D1a88654776eC0c86F08B"
ASTERDEX_API_KEY = "your_api_key"
ASTERDEX_API_SECRET = "your_api_secret"
GROK_API_KEY = "your_grok_key"
```

### 3. Test Before Going Live

```bash
source venv/bin/activate
python test_autonomous.py
```

This verifies:
- ✅ API connections work
- ✅ Can fetch market data
- ✅ Grok AI is responding
- ✅ Can check balance and positions

### 4. Start Trading 24/7

**Option A: Systemd (Recommended for VPS)**

```bash
sudo systemctl start cosmic-trader
sudo systemctl enable cosmic-trader  # Auto-start on boot
sudo systemctl status cosmic-trader  # Check status
```

**Option B: Docker**

```bash
docker-compose up -d
docker-compose logs -f  # Watch logs
```

**Option C: Manual (for testing)**

```bash
source venv/bin/activate
python autonomous_cosmic_trader.py
```

### 5. Monitor Logs

```bash
# Real-time logs
tail -f cosmic_trader.log

# Or with systemd
journalctl -u cosmic-trader -f
```

### 6. Deposit More Funds

Simply deposit more ETH to your AsterDEX Futures account at [asterdex.com](https://asterdex.com). The bot will automatically use available balance.

---

## Configuration Tuning

### Trading Frequency

Edit `config.py`:
```python
CHECK_INTERVAL_MINUTES = 30  # Check every 30 min
```

More frequent = more API calls = slightly higher Grok costs
Less frequent = fewer opportunities but cheaper

**Grok API Pricing:**
- ~$0.001 per decision (very cheap!)
- 48 checks/day (every 30 min) = ~$0.05/day
- ~$1.50/month total API costs

### Position Sizing

```python
POSITION_SIZE_USD = 10  # $10 per trade
```

With $13 balance, you can comfortably do $10 positions.
Add more funds to increase position size.

### Risk Management

```python
STOP_LOSS_PERCENT = 5.0     # Auto-exit at -5% loss
TAKE_PROFIT_PERCENT = 10.0  # Auto-exit at +10% profit
MAX_OPEN_POSITIONS = 3       # Max concurrent positions
```

Adjust based on your risk tolerance!

---

## Systemctl Commands Cheat Sheet

```bash
# Start the bot
sudo systemctl start cosmic-trader

# Stop the bot
sudo systemctl stop cosmic-trader

# Restart the bot
sudo systemctl restart cosmic-trader

# Check status
sudo systemctl status cosmic-trader

# View logs
journalctl -u cosmic-trader -f

# Enable auto-start on boot
sudo systemctl enable cosmic-trader

# Disable auto-start
sudo systemctl disable cosmic-trader
```

---

## Docker Commands Cheat Sheet

```bash
# Start in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Check status
docker-compose ps
```

---

## Troubleshooting

### "Permission denied" when starting systemd service

```bash
sudo systemctl start cosmic-trader
```

### Port already in use (Docker)

No ports needed! Bot just runs locally making API calls.

### Bot not making trades

1. Check logs: `tail -f cosmic_trader.log`
2. Verify balance: `python check_position.py`
3. Cosmos might be saying "PASS" - that's okay! It means no good vibes detected.

### Update the bot code

```bash
# On server
git pull origin main
sudo systemctl restart cosmic-trader
```

---

## Security Best Practices

1. **Never commit `config.py`** - Already in `.gitignore` ✅
2. **Use SSH keys** for server access
3. **Enable firewall** on your VPS
4. **Monitor logs** regularly for suspicious activity
5. **Start small** - test with minimal funds first

---

## Monitoring Dashboard (Optional)

Create a simple status script:

```bash
# status.sh
echo "🌙 Cosmic Trader Status"
echo "======================="
sudo systemctl status cosmic-trader --no-pager | head -20
echo ""
echo "Recent Logs:"
tail -20 cosmic_trader.log
```

Run with: `bash status.sh`

---

## Cost Breakdown

**Monthly Costs:**
- VPS: $5-10/month (e.g., DigitalOcean, Linode)
- Grok API: ~$1.50/month (very cheap!)
- AsterDEX trading fees: ~0.02% per trade

**Total: ~$7-12/month** for 24/7 autonomous cosmic trading 🌙

---

## What Happens Now?

Once started, the bot will:

1. **Every 30 minutes:**
   - Check all open positions
   - Ask Grok if positions should close
   - Auto-close on stop-loss/take-profit
   - Scan for new trade opportunities
   - Consult cosmos on each symbol
   - Open positions based on cosmic guidance

2. **Log everything:**
   - All decisions and reasons
   - Entry/exit prices
   - PnL tracking
   - Cosmic reasoning

3. **Auto-recover:**
   - Restarts on crashes
   - Handles API errors gracefully
   - Continues trading through network issues

**You literally just need to:**
- ✅ Deposit funds when needed
- ✅ Monitor logs occasionally
- ✅ Trust the universe 🌙✨

---

## Emergency Stop

If you need to stop trading immediately:

```bash
# Stop the bot
sudo systemctl stop cosmic-trader

# Close all positions manually
python check_position.py
# Then manually close via AsterDEX UI
```

---

## Final Checklist

Before going live:

- [ ] Repo cloned to server
- [ ] `setup_server.sh` executed successfully
- [ ] `test_autonomous.py` passes all tests
- [ ] Config file has correct API keys
- [ ] Sufficient ETH balance deposited
- [ ] Systemd service enabled and running
- [ ] Logs are being written
- [ ] Can view real-time logs with `tail -f`

Once all checked, you're ready! The cosmos will handle the rest. 🌌

---

*May the stars guide your autonomous trades to profit!* 🚀🌕
