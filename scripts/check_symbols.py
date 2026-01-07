"""
Check available trading symbols
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from asterdex_client import AsterDEXClient
import config

client = AsterDEXClient(
    base_url=config.ASTERDEX_BASE_URL,
    api_wallet=config.ASTERDEX_API_WALLET,
    private_key=config.ASTERDEX_PRIVATE_KEY
)

print("Fetching available symbols...")
exchange_info = client.get_exchange_info()

symbols = exchange_info.get('symbols', [])
print(f"\nFound {len(symbols)} symbols\n")

print("First 20 symbols:")
for i, symbol_info in enumerate(symbols[:20]):
    symbol = symbol_info.get('symbol', 'Unknown')
    status = symbol_info.get('status', 'Unknown')
    print(f"{i+1}. {symbol} - {status}")

print("\nSearching for BTC symbols...")
btc_symbols = [s for s in symbols if 'BTC' in s.get('symbol', '')]
print(f"Found {len(btc_symbols)} BTC symbols:")
for s in btc_symbols[:10]:
    print(f"  - {s.get('symbol')}")
