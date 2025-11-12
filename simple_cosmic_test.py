"""
Simple cosmic vibe check using basic ticker data
"""
from asterdex_client import AsterDEXClient
from grok_client import GrokClient
import config

print("="*60)
print("🌙 ✨ COSMIC VIBE CHECK ✨ 🌙")
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

print("\n📊 Fetching BTC market data...\n")

# Get ticker data
ticker = dex.get_ticker_24h("BTCUSDT")
price = dex.get_ticker_price("BTCUSDT")

market_data = {
    "symbol": "BTCUSDT",
    "price": price.get('price'),
    "price_change_24h": ticker.get('priceChangePercent'),
    "high_24h": ticker.get('highPrice'),
    "low_24h": ticker.get('lowPrice'),
    "volume_24h": ticker.get('volume'),
}

print("Market Data:")
for key, value in market_data.items():
    print(f"  {key}: {value}")

print("\n🔮 Channeling cosmic wisdom...\n")

# Get cosmic decision
decision = grok.get_trading_decision(market_data)

print("\n✨ The Universe Says:")
print(decision)

print("\n" + "="*60)
print("✨ The cosmos has spoken ✨")
print("="*60)
