"""
Cosmic Trading Test - Let the universe guide a real trade
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from asterdex_client import AsterDEXClient
from grok_client import GrokClient
import config
import json

print("="*60)
print("🌙 ✨ COSMIC TRADING RITUAL ✨ 🌙")
print("="*60)

# Initialize clients
dex = AsterDEXClient(
    base_url=config.ASTERDEX_BASE_URL,
    api_wallet=config.ASTERDEX_API_WALLET,
    private_key=config.ASTERDEX_PRIVATE_KEY
)

grok = GrokClient(
    api_key=config.GROK_API_KEY,
    base_url=config.GROK_BASE_URL,
    model=config.GROK_MODEL
)

print("\n💰 Checking your cosmic wallet energy...\n")

# Check balance
try:
    balance = dex.get_balance()
    print("Balance Info:")
    print(json.dumps(balance, indent=2))
except Exception as e:
    print(f"Error checking balance: {e}")

print("\n📊 Checking your current positions...\n")

# Check positions
try:
    positions = dex.get_position_risk()
    print("Current Positions:")
    print(json.dumps(positions, indent=2))
except Exception as e:
    print(f"Error checking positions: {e}")

print("\n🔮 Let's ask the cosmos what to trade...\n")

# Get available symbols with good liquidity
symbols_to_check = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

print("Scanning the celestial charts for these symbols:")
for sym in symbols_to_check:
    print(f"  🌟 {sym}")

print("\n📈 Fetching market data for cosmic analysis...\n")

# Get market data for symbols
market_data = {}
for symbol in symbols_to_check:
    try:
        ticker = dex.get_ticker_24h(symbol)
        price = dex.get_ticker_price(symbol)

        market_data[symbol] = {
            "price": price.get('price'),
            "price_change_24h": ticker.get('priceChangePercent'),
            "volume_24h": ticker.get('volume'),
        }
        print(f"{symbol}: ${price.get('price')} ({ticker.get('priceChangePercent')}%)")
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

print("\n🌙 Channeling cosmic wisdom for trading decision...\n")

# Ask Grok which one to trade
cosmic_prompt = f"""
The cosmic trader has $13 to test the universe's guidance.

Available symbols and their energies:
{json.dumps(market_data, indent=2)}

Which symbol has the best cosmic energy right now?
Should we go LONG or SHORT?
What's the vibe? Keep it mellow and mystical.

Remember: we only have $13, so this is a small test to see if the stars align.
Give me ONE clear recommendation: which symbol and which direction (LONG/SHORT).
"""

cosmic_decision = grok.quick_decision(cosmic_prompt)
print("✨ The Universe Says:")
print(cosmic_decision)

print("\n" + "="*60)
print("\nNOTE: Check the cosmic advice above.")
print("To execute a trade manually, use: python trading_bot.py")
print("Select option 7 for manual trade execution.")
print("\nFor a tiny test trade, try:")
print("  - Symbol: (what the cosmos suggested)")
print("  - Side: BUY (for LONG) or SELL (for SHORT)")
print("  - Type: MARKET")
print("  - Quantity: 0.001 (very small test)")
print("="*60)
