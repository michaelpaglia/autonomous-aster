# Autonomous Cosmic Trader

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AsterDEX](https://img.shields.io/badge/Exchange-AsterDEX-purple.svg)](https://asterdex.com)
[![xAI Grok](https://img.shields.io/badge/AI-xAI%20Grok-orange.svg)](https://x.ai)

An autonomous cryptocurrency trading bot for [AsterDEX](https://asterdex.com) that makes decisions using xAI's Grok model with an astrology-themed decision framework. The bot operates 24/7, analyzing market conditions through a unique "cosmic vibes" lens.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Autonomous 24/7 Trading** - Runs continuously with configurable check intervals
- **AI-Powered Decisions** - Uses xAI Grok for market analysis and trade decisions
- **Multi-Symbol Support** - Trade 230+ perpetual futures pairs simultaneously
- **Balance-Aware Sizing** - Automatically adjusts position sizes based on available capital
- **Real-Time Dashboard** - Next.js dashboard for monitoring trades and performance
- **Multiple Deployment Options** - Systemd, Docker, or manual execution
- **Comprehensive Logging** - Full audit trail of all decisions and trades

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | Required |
| Node.js | 18+ | For dashboard only |
| AsterDEX Account | - | [Sign up](https://asterdex.com) |
| xAI API Key | - | [Get key](https://x.ai) |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/michaelpaglia/autonomous-aster.git
cd autonomous-aster
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install git+https://github.com/asterdex/aster-connector-python.git
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# AsterDEX API Configuration
ASTERDEX_BASE_URL=https://fapi.asterdex.com
ASTERDEX_MAIN_WALLET=your_main_wallet_address
ASTERDEX_API_WALLET=your_api_wallet_address
ASTERDEX_PRIVATE_KEY=your_private_key
ASTERDEX_API_KEY=your_api_key
ASTERDEX_API_SECRET=your_api_secret

# xAI Grok Configuration
GROK_API_KEY=your_grok_api_key
GROK_BASE_URL=https://api.x.ai/v1
GROK_MODEL=grok-4-fast-non-reasoning

# Trading Configuration
CHECK_INTERVAL_MINUTES=10
USE_ALL_SYMBOLS=True
MAX_OPEN_POSITIONS=3
MIN_BALANCE_USD=1
```

### 5. Verify Installation

```bash
python tests/test_connections.py
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHECK_INTERVAL_MINUTES` | How often to check for trades | `10` |
| `USE_ALL_SYMBOLS` | Trade all available symbols | `True` |
| `MAX_OPEN_POSITIONS` | Maximum concurrent positions | `3` |
| `MIN_BALANCE_USD` | Minimum balance to continue trading | `1` |
| `LEVERAGE_MIN` | Minimum leverage multiplier | `10` |
| `LEVERAGE_MAX` | Maximum leverage multiplier | `20` |
| `MIN_POSITION_NOTIONAL` | Minimum position value (USD) | `5.5` |

### Manual Symbol Selection

To trade specific symbols only, set `USE_ALL_SYMBOLS=False` and edit `src/config.py`:

```python
TRADING_SYMBOLS = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
]
```

---

## Usage

### Start the Bot

```bash
# Recommended: Use the main entry point
python main.py

# Or activate venv first
source venv/bin/activate
python main.py
```

### Run Tests

```bash
# Test API connections
python tests/test_connections.py

# Test balance check
python tests/test_balance.py

# Validate bot configuration
python tests/validate_bot.py
```

### Utility Scripts

```bash
# List available trading symbols
python scripts/list_symbols.py

# Check current positions
python scripts/check_position.py

# Run demo
python scripts/demo.py
```

---

## Project Structure

```
aster-dex/
├── src/                          # Core application modules
│   ├── __init__.py
│   ├── autonomous_cosmic_trader.py   # Main trading bot
│   ├── asterdex_client.py            # AsterDEX API client
│   ├── grok_client.py                # xAI Grok client
│   ├── config.py                     # Configuration loader
│   ├── stats_exporter.py             # Dashboard stats export
│   └── trading_bot.py                # Trading bot utilities
│
├── tests/                        # Test files
│   ├── test_connections.py
│   ├── test_balance.py
│   ├── test_autonomous.py
│   └── ...
│
├── scripts/                      # Utility scripts
│   ├── setup_server.sh               # Server setup script
│   ├── sync_stats.sh                 # Stats sync for dashboard
│   ├── list_symbols.py
│   ├── check_position.py
│   └── demo.py
│
├── deploy/                       # Deployment configurations
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── cosmic-trader.service         # Systemd service
│
├── docs/                         # Documentation
│   ├── DEPLOYMENT.md
│   ├── BALANCE_FEATURES.md
│   ├── SYMBOLS_GUIDE.md
│   ├── CRON_SETUP.md
│   └── WINDOWS_SETUP.md
│
├── dashboard/                    # Next.js monitoring dashboard
│   ├── app/
│   ├── public/
│   └── package.json
│
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── LICENSE
```

---

## Deployment

### Option 1: Systemd (Recommended for VPS)

```bash
# Run setup script
cd scripts
chmod +x setup_server.sh
./setup_server.sh

# Control the service
sudo systemctl start cosmic-trader
sudo systemctl stop cosmic-trader
sudo systemctl restart cosmic-trader
sudo systemctl status cosmic-trader

# Enable auto-start on boot
sudo systemctl enable cosmic-trader
```

### Option 2: Docker

```bash
cd deploy

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 3: Manual

```bash
source venv/bin/activate
python main.py
```

For detailed deployment instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

---

## Monitoring

### View Logs

```bash
# Real-time logs
tail -f cosmic_trader.log

# With systemd
journalctl -u cosmic-trader -f

# With Docker
docker-compose logs -f
```

### Dashboard

The project includes a Next.js dashboard for real-time monitoring:

```bash
cd dashboard
npm install
npm run dev
```

Access at `http://localhost:3000`

For Vercel deployment, see [dashboard/VERCEL_SETUP.md](dashboard/VERCEL_SETUP.md).

### Check Status

```bash
# Systemd
sudo systemctl status cosmic-trader

# Docker
docker-compose ps

# Manual position check
python scripts/check_position.py
```

---

## API Reference

### AsterDEXClient

```python
from src.asterdex_client import AsterDEXClient

client = AsterDEXClient(
    base_url="https://fapi.asterdex.com",
    api_wallet="0x...",
    private_key="0x..."
)

# Get balance
balance = client.get_balance()

# Get positions
positions = client.get_position_risk()

# Place order
order = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.001
)
```

### GrokClient

```python
from src.grok_client import GrokClient

grok = GrokClient(
    api_key="your_api_key",
    base_url="https://api.x.ai/v1",
    model="grok-4-fast-non-reasoning"
)

# Get trading decision
decision = grok.get_trading_decision(market_data)
```

---

## Troubleshooting

### Bot not starting?

```bash
# Check logs
tail -f cosmic_trader.log

# Test API connections
python tests/test_connections.py

# Verify config
python tests/validate_bot.py
```

### No trades happening?

1. Verify sufficient balance in AsterDEX account
2. Check `MIN_BALANCE_USD` setting
3. Review logs for "PASS" decisions (bot waiting for better conditions)

### Import errors?

Ensure you're running from the project root:

```bash
cd /path/to/aster-dex
python main.py
```

### Connection issues?

```bash
# Test AsterDEX API
python tests/test_official_connector.py

# Check network
curl -I https://fapi.asterdex.com
```

---

## Safety Considerations

> **Warning**: This bot trades with real funds. Use at your own risk.

- Start with small amounts to test
- Monitor the bot regularly
- Set appropriate `MAX_OPEN_POSITIONS` limits
- Keep API keys secure and never commit them to version control
- The `.env` file is gitignored for your protection

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [AsterDEX](https://asterdex.com) - Decentralized perpetual futures exchange
- [xAI](https://x.ai) - Grok AI model provider
- [aster-connector-python](https://github.com/asterdex/aster-connector-python) - Official AsterDEX Python SDK
