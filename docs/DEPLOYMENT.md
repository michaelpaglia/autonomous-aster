# Server Deployment Guide

## Quick Deploy

### 1. Clone and Setup

```bash
# Clone the repo
git clone <your-github-repo-url>
cd aster-dex

# Run automated setup
cd scripts
chmod +x setup_server.sh
./setup_server.sh
```

The setup script will:
- Install Python 3.11 and dependencies
- Create a virtual environment
- Install all required packages
- Optionally set up systemd service for auto-start

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your credentials
nano .env
```

Required environment variables:
- `ASTERDEX_MAIN_WALLET` - Your main trading wallet address
- `ASTERDEX_API_WALLET` - Your API signer wallet
- `ASTERDEX_API_KEY` - AsterDEX API key
- `ASTERDEX_API_SECRET` - AsterDEX API secret
- `ASTERDEX_PRIVATE_KEY` - Your private key
- `GROK_API_KEY` - xAI Grok API key

### 3. Test Before Going Live

```bash
source venv/bin/activate
python tests/test_autonomous.py
```

This verifies:
- API connections work
- Can fetch market data
- Grok AI is responding
- Can check balance and positions

### 4. Start Trading

**Option A: Systemd (Recommended)**

```bash
sudo systemctl start cosmic-trader
sudo systemctl enable cosmic-trader  # Auto-start on boot
sudo systemctl status cosmic-trader  # Check status
```

**Option B: Docker**

```bash
cd deploy
docker-compose up -d
docker-compose logs -f  # Watch logs
```

**Option C: Manual**

```bash
source venv/bin/activate
python main.py
```

### 5. Monitor Logs

```bash
# Real-time logs
tail -f cosmic_trader.log

# With systemd
journalctl -u cosmic-trader -f

# With Docker
cd deploy && docker-compose logs -f
```

---

## Configuration

### Trading Frequency

Edit `.env`:
```env
CHECK_INTERVAL_MINUTES=30  # Check every 30 min
```

- More frequent = more API calls = slightly higher costs
- Less frequent = fewer opportunities but cheaper

**Grok API Pricing:**
- ~$0.001 per decision
- 48 checks/day (every 30 min) = ~$0.05/day
- ~$1.50/month total API costs

### Risk Management

Edit `.env`:
```env
MAX_OPEN_POSITIONS=3
MIN_BALANCE_USD=1
LEVERAGE_MIN=10
LEVERAGE_MAX=20
```

---

## Systemctl Commands

```bash
sudo systemctl start cosmic-trader     # Start
sudo systemctl stop cosmic-trader      # Stop
sudo systemctl restart cosmic-trader   # Restart
sudo systemctl status cosmic-trader    # Status
journalctl -u cosmic-trader -f         # View logs
sudo systemctl enable cosmic-trader    # Enable auto-start
sudo systemctl disable cosmic-trader   # Disable auto-start
```

---

## Docker Commands

```bash
cd deploy
docker-compose up -d           # Start
docker-compose down            # Stop
docker-compose logs -f         # Logs
docker-compose restart         # Restart
docker-compose ps              # Status
```

---

## Troubleshooting

### "Permission denied" with systemd

```bash
sudo systemctl start cosmic-trader
```

### Bot not making trades

1. Check logs: `tail -f cosmic_trader.log`
2. Verify balance: `python scripts/check_position.py`
3. Review decisions in logs - the AI may be deciding to wait

### Update the bot

```bash
git pull origin main
sudo systemctl restart cosmic-trader
```

---

## Security Best Practices

1. Never commit `.env` to version control
2. Use SSH keys for server access
3. Enable firewall on your VPS
4. Monitor logs regularly
5. Start with minimal funds for testing

---

## Cost Breakdown

**Monthly Costs:**
- VPS: $5-10/month (DigitalOcean, Linode, etc.)
- Grok API: ~$1.50/month
- AsterDEX trading fees: ~0.02% per trade

**Total: ~$7-12/month**

---

## Emergency Stop

```bash
# Stop the bot immediately
sudo systemctl stop cosmic-trader

# Check and close positions manually
python scripts/check_position.py
# Then close via AsterDEX UI if needed
```

---

## Deployment Checklist

- [ ] Repository cloned to server
- [ ] `setup_server.sh` executed successfully
- [ ] `.env` configured with credentials
- [ ] `tests/test_autonomous.py` passes
- [ ] Sufficient ETH balance deposited
- [ ] Systemd service enabled and running
- [ ] Logs are being written
- [ ] Can view real-time logs
