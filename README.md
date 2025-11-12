# AsterDEX Trading Bot with Grok AI

An AI-powered cryptocurrency trading bot that uses xAI's Grok language model to make trading decisions on the AsterDEX perpetual futures exchange.

## Features

- **AsterDEX API Integration**: Full Web3 ECDSA signature authentication
- **Grok AI Integration**: Uses Grok Fast Non-reasoning model for trading decisions
- **Market Data Analysis**: Real-time price data, order books, and 24h statistics
- **Account Management**: View balances, positions, and trade history
- **Interactive CLI**: User-friendly menu-driven interface
- **Manual & AI Trading**: Execute trades manually or let Grok decide

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/michaelpaglia/Desktop/aster-dex
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration is already set up in `config.py`** with your credentials

## Usage

### Run the Trading Bot

```bash
python trading_bot.py
```

### Menu Options

1. **Test API Connections** - Verify both AsterDEX and Grok APIs are working
2. **Get Account Summary** - View your balance and open positions
3. **Get Market Data** - Fetch real-time data for any trading pair
4. **Ask Grok for Advice** - Get AI insights on any trading question
5. **AI Trading Decision** - Let Grok analyze market data and recommend a trade
6. **View Open Positions** - See all your current positions
7. **Execute Manual Trade** - Place orders directly (use with caution)

## Quick Start

1. Run the bot:
   ```bash
   python trading_bot.py
   ```

2. Select option `1` to test API connections

3. Try option `5` to get an AI trading recommendation for a symbol like `BTCUSDT`

## API Clients

### AsterDEX Client (`asterdex_client.py`)

Handles all interactions with the AsterDEX Futures API v3:
- Web3 ECDSA signature authentication
- Market data endpoints (prices, order book, trades)
- Trading endpoints (place/cancel orders)
- Account endpoints (balance, positions, leverage)

Example usage:
```python
from asterdex_client import AsterDEXClient

client = AsterDEXClient(
    base_url="https://fapi.asterdex.com",
    api_wallet="0xYourWallet",
    private_key="0xYourPrivateKey"
)

# Get market data
ticker = client.get_ticker_24h("BTCUSDT")
print(ticker)

# Place an order
order = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.001
)
```

### Grok Client (`grok_client.py`)

Interfaces with xAI's Grok API for AI-powered trading insights:
- OpenAI-compatible API
- Trading decision analysis
- Position management recommendations
- Custom queries

Example usage:
```python
from grok_client import GrokClient

client = GrokClient(
    api_key="xai-YourKey",
    model="grok-beta"
)

# Get trading advice
response = client.get_trading_decision(
    market_data={"price": 50000, "change_24h": "+5%"},
    context="Should I go long on BTC?"
)
print(response)
```

## Project Structure

```
aster-dex/
├── README.md              # This file
├── START_HERE.md          # Project goals and docs
├── requirements.txt       # Python dependencies
├── config.py             # API credentials (gitignored)
├── asterdex_client.py    # AsterDEX API client
├── grok_client.py        # Grok AI client
└── trading_bot.py        # Main bot script
```

## Configuration

Your credentials are stored in `config.py`:
- AsterDEX API wallet address and private key
- xAI Grok API key
- Base URLs for both services

**⚠️ SECURITY NOTE**: `config.py` is gitignored. Never commit credentials to version control.

## Safety Features

- Manual trade confirmations required
- Clear warnings for dangerous operations
- Read-only mode by default (viewing data)
- Explicit user consent for all trades

## Development

### Testing Connections

```bash
python trading_bot.py
# Select option 1
```

### Getting Market Data

The bot can fetch:
- 24-hour price statistics
- Current mark price
- Order book depth
- Recent trades
- Funding rates

### AI Trading Workflow

1. Fetch real-time market data for a symbol
2. Send data to Grok with trading context
3. Receive AI analysis and recommendation
4. (Optional) Execute trade based on recommendation

## Troubleshooting

### API Connection Failed

- **AsterDEX**: Check that your API wallet address and private key are correct
- **Grok**: Verify your xAI API key is valid and has sufficient credits

### Signature Errors

The AsterDEX API uses Web3 ECDSA signatures. Ensure:
- Private key has correct format (with 0x prefix)
- System time is synchronized (nonce must be within 5 seconds of server time)

### Module Not Found

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Next Steps

- Add automated trading strategies
- Implement risk management rules
- Set up trading signals and alerts
- Create backtesting framework
- Add Telegram/Discord notifications

## Resources

- [AsterDEX API Documentation](https://github.com/asterdex/api-docs)
- [xAI Grok API](https://x.ai/api)

## Disclaimer

**⚠️ USE AT YOUR OWN RISK**: This bot is for educational and experimental purposes. Cryptocurrency trading carries significant risk. Always test with small amounts first and never trade more than you can afford to lose.
