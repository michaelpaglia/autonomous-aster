"""
List all available trading symbols on AsterDEX
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from aster.rest_api import Client
import config

print("="*60)
print("📊 Available Trading Symbols on AsterDEX")
print("="*60)

client = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)

# Get exchange info
exchange_info = client.exchange_info()
symbols = exchange_info.get('symbols', [])

# Filter to only TRADING status
trading_symbols = [s for s in symbols if s.get('status') == 'TRADING']

print(f"\n✨ Found {len(trading_symbols)} actively trading symbols!\n")

# Group by base asset
btc_symbols = []
eth_symbols = []
sol_symbols = []
other_symbols = []

for s in trading_symbols:
    symbol = s.get('symbol')
    if 'BTC' in symbol:
        btc_symbols.append(symbol)
    elif 'ETH' in symbol:
        eth_symbols.append(symbol)
    elif 'SOL' in symbol:
        sol_symbols.append(symbol)
    else:
        other_symbols.append(symbol)

# Display by category
if btc_symbols:
    print("🟠 BTC Symbols:")
    for sym in btc_symbols[:10]:
        print(f"  - {sym}")
    if len(btc_symbols) > 10:
        print(f"  ... and {len(btc_symbols) - 10} more")

if eth_symbols:
    print("\n🔵 ETH Symbols:")
    for sym in eth_symbols[:10]:
        print(f"  - {sym}")
    if len(eth_symbols) > 10:
        print(f"  ... and {len(eth_symbols) - 10} more")

if sol_symbols:
    print("\n🟣 SOL Symbols:")
    for sym in sol_symbols[:10]:
        print(f"  - {sym}")
    if len(sol_symbols) > 10:
        print(f"  ... and {len(sol_symbols) - 10} more")

print("\n🌈 Popular Alt Symbols:")
popular = ['DOGEUSDT', 'XRPUSDT', 'ADAUSDT', 'BNBUSDT', 'AVAXUSDT',
           'LINKUSDT', 'DOTUSDT', 'MATICUSDT', 'UNIUSDT', 'LTCUSDT']
for sym in popular:
    if sym in [s.get('symbol') for s in trading_symbols]:
        print(f"  - {sym}")

print("\n" + "="*60)
print("📝 To add symbols to your bot:")
print("="*60)
print("1. Edit config.py")
print("2. Add symbols to TRADING_SYMBOLS list:")
print("   TRADING_SYMBOLS = [")
print("       'BTCUSDT',")
print("       'ETHUSDT',")
print("       'DOGEUSDT',  # Add any symbol from above!")
print("       # etc...")
print("   ]")
print("3. Restart bot: sudo systemctl restart cosmic-trader")
print("="*60)

print("\n🌙 All symbols available for cosmic trading!")
print(f"Total: {len(trading_symbols)} symbols")
print("\nThe universe has many paths to profit! ✨")
