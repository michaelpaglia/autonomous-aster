# Quick Start Guide

## What's Built

Your AI-powered trading bot is fully operational with:

✅ **AsterDEX API** - Connected and authenticated with Web3 ECDSA signatures
✅ **Grok AI** - Using `grok-4-fast-non-reasoning` model
✅ **Trading Bot** - Interactive CLI for AI-assisted trading

## Files Created

```
aster-dex/
├── asterdex_client.py       # AsterDEX API client with full trading capabilities
├── grok_client.py            # Grok AI client for trading decisions
├── trading_bot.py            # Main interactive trading bot
├── config.py                 # Your API credentials (gitignored)
├── test_connections.py       # Quick connection test
├── demo.py                   # Full feature demo
├── requirements.txt          # Python dependencies
├── .gitignore               # Protects credentials
├── README.md                 # Full documentation
└── QUICKSTART.md            # This file
```

## Quick Commands

### 1. Test Connections
```bash
python test_connections.py
```
Verifies both APIs are working.

### 2. Run Full Demo
```bash
python demo.py
```
Shows all features:
- Connection tests
- Account summary
- Market data fetch
- Grok AI advice
- AI trading decision

### 3. Interactive Trading Bot
```bash
python trading_bot.py
```
Opens the full menu with options:
- Get market data
- Ask Grok for advice
- AI trading decisions
- Manual trade execution
- View positions

## Example Usage

### Get AI Trading Decision
```bash
python trading_bot.py
# Select option 5
# Enter symbol: BTCUSDT
```

The bot will:
1. Fetch real-time market data (price, 24h change, volume, order book)
2. Send data to Grok for analysis
3. Receive AI recommendation (LONG/SHORT/HOLD)

### Ask Grok Custom Questions
```bash
python trading_bot.py
# Select option 4
# Ask: "Should I trade BTC or ETH right now?"
```

### View Your Account
```bash
python trading_bot.py
# Select option 2
```
Shows your balance and open positions.

## API Capabilities

### AsterDEX (asterdex_client.py)
**Market Data:**
- `get_ticker_24h()` - 24-hour statistics
- `get_mark_price()` - Current mark price
- `get_order_book()` - Order book depth
- `get_recent_trades()` - Recent trade history

**Trading:**
- `place_order()` - Place MARKET/LIMIT orders
- `cancel_order()` - Cancel specific order
- `cancel_all_orders()` - Cancel all orders
- `get_open_orders()` - View open orders

**Account:**
- `get_balance()` - Account balance
- `get_position_risk()` - Position details
- `set_leverage()` - Change leverage

### Grok AI (grok_client.py)
- `get_trading_decision()` - Analysis with market data
- `analyze_position()` - Position management advice
- `quick_decision()` - Answer any trading question

## Safety Features

⚠️ **The bot is read-only by default** - viewing data is safe
⚠️ **Manual trades require confirmation** - you must type "yes"
⚠️ **AI decisions are advisory only** - bot won't auto-trade without your command

## Current Configuration

- **Model:** grok-4-fast-non-reasoning (fast, non-reasoning for quick decisions)
- **Exchange:** AsterDEX Perpetual Futures
- **Auth:** Web3 ECDSA signatures (secure, decentralized)

## Next Steps

1. **Test it out:** Run `python demo.py` to see everything in action
2. **Explore:** Use `python trading_bot.py` for interactive trading
3. **Customize:** Modify prompts in `grok_client.py` to change AI behavior
4. **Extend:** Add automated strategies to `trading_bot.py`

## Need Help?

- Check `README.md` for detailed documentation
- Review API docs: https://github.com/asterdex/api-docs
- Test with small amounts first!

---

**Status:** 🟢 All systems operational
**Last tested:** Successfully connected to both APIs
**Ready to trade!** 🚀
