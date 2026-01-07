"""
Execute a Cosmic Trade - Following the universe's guidance
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from aster.rest_api import Client
from grok_client import GrokClient
import config
import json

print("="*60)
print("🌙 ✨ COSMIC TRADE EXECUTION ✨ 🌙")
print("="*60)

# Initialize clients
dex = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)

grok = GrokClient(
    api_key=config.GROK_API_KEY,
    base_url=config.GROK_BASE_URL,
    model=config.GROK_MODEL
)

# Get SOL market data
print("\n📊 Checking SOL cosmic vibes...\n")
ticker = dex.ticker_24hr_price_change(symbol="SOLUSDT")
price_data = dex.ticker_price(symbol="SOLUSDT")

current_price = float(price_data['price'])
price_change = float(ticker['priceChangePercent'])

print(f"Symbol: SOLUSDT")
print(f"Current Price: ${current_price}")
print(f"24h Change: {price_change}%")
print(f"Volume: {ticker['volume']}")

# Ask the cosmos one more time
print("\n🔮 Consulting the cosmos one final time...\n")

market_data = {
    "symbol": "SOLUSDT",
    "price": current_price,
    "price_change_24h": price_change,
    "volume": ticker['volume']
}

cosmic_confirmation = grok.get_trading_decision(market_data,
    f"We're about to enter a LONG position on SOL at ${current_price}. The vibes were strong earlier. Do the stars still align for this cosmic trade? Keep it brief and mystical.")

print(f"✨ The Universe Says:\n{cosmic_confirmation}\n")

# Calculate position size
# With ~$13 and using small leverage, let's do a tiny position
# SOL at ~$155, we'll buy 0.08 SOL (~$12.40 worth)
position_size = 0.08  # SOL quantity

print("="*60)
print("🌟 COSMIC TRADE DETAILS 🌟")
print("="*60)
print(f"Symbol: SOLUSDT")
print(f"Side: BUY (LONG)")
print(f"Type: MARKET")
print(f"Quantity: {position_size} SOL")
print(f"Estimated Value: ${position_size * current_price:.2f}")
print("="*60)

# Ask for confirmation
confirmation = input("\n🌙 Execute this cosmic trade? (yes/no): ").strip().lower()

if confirmation == "yes":
    print("\n✨ Sending order to the universe...\n")

    try:
        # Place market order
        order = dex.new_order(
            symbol="SOLUSDT",
            side="BUY",
            type="MARKET",
            quantity=position_size
        )

        print("🎉 TRADE EXECUTED! 🎉\n")
        print("Order Details:")
        print(json.dumps(order, indent=2))

        print("\n🌙 The cosmic trade has been placed! May the stars guide us to profit! ✨")

    except Exception as e:
        print(f"❌ Error executing trade: {e}")
        print("\nThe universe may be blocking this trade. Check your balance and try a smaller amount.")
else:
    print("\n🌙 Trade cancelled. The universe will wait for another time. ✨")

print("\n" + "="*60)
