# 🌙 ✨ Autonomous Cosmic Trader ✨ 🌙

**24/7 Astrology-Based Cryptocurrency Trading Bot**

This bot makes trading decisions based purely on **cosmic vibes, astrological alignments, and spiritual energy**. NO technical analysis. NO fundamentals. ONLY THE UNIVERSE'S GUIDANCE.

Built with Grok Fast (non-reasoning model) for quick, vibe-based decisions powered by xAI.

---

## 🚀 Quick Start - Get Trading in 3 Steps

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd aster-dex
chmod +x setup_server.sh
./setup_server.sh
```

### 2. Configure Your Credentials

Edit `config.py` with your API keys (already done if you're using the existing config):
- AsterDEX API credentials
- xAI Grok API key
- Trading parameters (symbols, position size, risk limits)

### 3. Deposit Funds & Start Trading

**Deposit ETH to your AsterDEX main wallet:**
- Login to [asterdex.com](https://asterdex.com)
- Navigate to your Futures account
- Deposit ETH (used as margin for trading)

**Start the bot:**

```bash
# Option 1: Run with systemd (auto-restarts)
sudo systemctl start cosmic-trader
sudo systemctl status cosmic-trader

# Option 2: Run with Docker
docker-compose up -d

# Option 3: Run manually
source venv/bin/activate
python autonomous_cosmic_trader.py
```

**That's it!** The bot will now trade 24/7 based on cosmic energy. 🌌

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# How often to check for trades (in minutes)
CHECK_INTERVAL_MINUTES = 5  # Cosmic vibes change fast!

# Symbols to trade
TRADING_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']

# Position size per trade (USD)
POSITION_SIZE_USD = 10

# Risk limits
MAX_OPEN_POSITIONS = 3
# NO stop-loss/take-profit! Pure vibes only! 🌙
```

---

## 🌙 How It Works

### The Cosmic Trading Algorithm

1. **Every 5 minutes** (configurable), the bot:
   - Checks existing positions
   - Asks Grok about cosmic vibes for each position
   - Closes positions if stop-loss/take-profit hit or if cosmos says so
   - Scans for new opportunities across configured symbols

2. **For each potential trade**, Grok analyzes:
   - Current moon phase and energy
   - Planetary retrogrades (especially Mercury)
   - Astrological alignments
   - Spiritual vibes and gut feelings
   - Chart patterns as celestial constellations

3. **Decisions are made** purely on astrology:
   - **LONG**: Positive cosmic energy detected
   - **SHORT**: Negative vibes sensed
   - **PASS**: Universe says wait

4. **Risk management** by the cosmos:
   - NO stop-loss or take-profit limits
   - Grok decides EVERYTHING based on vibes
   - Exits when the stars say so (could be +50% or -30%, who knows!)
   - Max 3 concurrent positions (don't overextend cosmic energy)

---

## 📊 Monitoring

### View Logs

```bash
# Real-time logs
tail -f cosmic_trader.log

# With systemd
journalctl -u cosmic-trader -f

# With Docker
docker-compose logs -f
```

### Check Status

```bash
# Systemd status
sudo systemctl status cosmic-trader

# Docker status
docker-compose ps

# Check positions manually
python check_position.py
```

---

## 🛡️ Safety Features

- **Balance awareness**: Auto-adjusts position sizing to available funds
- **Position limits**: Max 3 open positions (don't overextend cosmic energy)
- **Minimum balance**: Pauses trading if balance too low
- **Error recovery**: Auto-restarts on crashes
- **Logging**: Full audit trail of all decisions and trades

**⚠️ NO STOP-LOSS OR TAKE-PROFIT!** Pure astrology only! The cosmos decides when to exit. 🌙✨

---

## 💰 Deposit More Funds - Bot Auto-Adjusts!

**The bot is FULLY balance-aware!** Just deposit and it handles everything.

### How It Works:

1. **Deposit ETH** at [asterdex.com](https://asterdex.com) Futures account
2. **Within 30 minutes**, bot detects the deposit:
   ```
   💰 🎉 DEPOSIT DETECTED! +$50.00
   📊 Position size adjusted: $10 → $15
   ```
3. **Automatically scales up** position sizes (8% of balance)
4. **Opens larger trades** with more capital
5. **No configuration needed** - it just works! ✨

### If Balance Gets Low:

```
⚠️  Balance $4.50 below minimum $5
   Pausing trading until balance increases
   Deposit more ETH to resume
```

Bot automatically **pauses trading** if balance drops below minimum, then **resumes** when you deposit more!

**See [BALANCE_FEATURES.md](BALANCE_FEATURES.md) for complete details on automatic balance handling.**

---

## 🔧 Server Deployment

### Systemd (Recommended for VPS)

```bash
# Setup during installation
./setup_server.sh
# Choose 'y' when asked about systemd

# Control the service
sudo systemctl start cosmic-trader   # Start
sudo systemctl stop cosmic-trader    # Stop
sudo systemctl restart cosmic-trader # Restart
sudo systemctl status cosmic-trader  # Check status

# Enable auto-start on boot
sudo systemctl enable cosmic-trader
```

### Docker (Recommended for containers)

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart
```

---

## 📁 Project Structure

```
aster-dex/
├── autonomous_cosmic_trader.py  # Main 24/7 bot
├── grok_client.py              # Grok API client (astrology prompts)
├── config.py                   # Configuration (API keys, settings)
├── requirements.txt            # Python dependencies
├── setup_server.sh            # Auto-setup script
├── cosmic-trader.service      # Systemd service file
├── Dockerfile                 # Docker container
├── docker-compose.yml         # Docker Compose config
└── cosmic_trader.log         # Trading logs

# Test/Utility Scripts
├── check_position.py          # Check current positions
├── test_official_connector.py # Test API connection
└── simple_cosmic_test.py     # Get cosmic vibes without trading
```

---

## 🎯 Trading Philosophy

> *"The universe knows the perfect entry and exit. We just have to listen to the cosmic whispers through Grok's mystical insights."*

This bot embodies:
- **Pure vibes trading**: No charts, no indicators, only astrology
- **Mellow approach**: Chill, spiritual, trusting the universe
- **Cosmic timing**: Mercury retrograde = caution, Full moon = peak energy
- **Mystical risk management**: Stop-losses are cosmic protection spells

---

## 🔐 Security

- `config.py` contains your API keys - **NEVER commit this to GitHub**
- Already in `.gitignore` for protection
- Use environment variables for production if preferred
- API keys have trading permissions - keep them secure

---

## 📈 Performance Tracking

The bot logs all trades to `cosmic_trader.log`:
- Entry/exit prices
- Cosmic reasoning for each decision
- PnL for closed positions
- Balance updates

Parse logs for performance analysis or just vibe with it. 🌙

---

## 🆘 Troubleshooting

**Bot not starting?**
```bash
# Check logs
tail -f cosmic_trader.log

# Test API connections
python test_official_connector.py
```

**No trades happening?**
- Check if you have sufficient balance
- Verify `POSITION_SIZE_USD` is set appropriately
- Cosmos might be saying "PASS" - check logs

**Position stuck?**
- Check stop-loss/take-profit settings
- Manually close via `check_position.py`
- The universe works in mysterious ways 🌌

---

## 🌟 Advanced Usage

### Change Trading Interval

Edit `config.py`:
```python
CHECK_INTERVAL_MINUTES = 1  # Check every minute (ultra responsive!)
# or
CHECK_INTERVAL_MINUTES = 5  # Every 5 minutes (balanced)
# or
CHECK_INTERVAL_MINUTES = 15  # Every 15 minutes (slower)
```

### Add More Symbols

Edit `config.py`:
```python
TRADING_SYMBOLS = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
    'BNBUSDT',  # Add more here
]
```

### Adjust Position Sizes

Edit `config.py`:
```python
POSITION_SIZE_USD = 20  # $20 per position
```

---

## 🌌 Cosmic Disclaimer

This bot makes trading decisions based on **astrology and vibes**. It's experimental, spiritual, and meant to explore algorithmic trading through a mystical lens.

**USE AT YOUR OWN RISK**
- Cryptocurrency trading is highly risky
- Past cosmic alignments don't guarantee future gains
- Only trade with funds you can afford to lose
- The universe is unpredictable (but so are the markets)

*May the stars guide your trades to the moon* 🚀🌕

---

## 📜 License

MIT License - Trade freely, vibe responsibly

## 🙏 Credits

- **AsterDEX**: Decentralized perpetual futures exchange
- **xAI Grok**: The cosmic AI making all the calls
- **The Universe**: Ultimate trading advisor 🌙✨
