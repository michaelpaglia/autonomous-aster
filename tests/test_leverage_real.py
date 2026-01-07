"""
Test actual leverage settings on AsterDEX
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from aster.rest_api import Client
import config

dex = Client(key=config.ASTERDEX_API_KEY, secret=config.ASTERDEX_API_SECRET)

# Test a few symbols
test_symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'ASTERUSDT']

print("="*60)
print("LEVERAGE TESTING")
print("="*60)

for symbol in test_symbols:
    try:
        # Check leverage brackets for this symbol
        print(f"\n{symbol}:")
        brackets = dex.leverage_brackets(symbol=symbol)
        print(f"  Leverage brackets: {brackets}")

        # Try to change leverage to 20x
        for lev in [20, 15, 10, 5]:
            try:
                result = dex.change_leverage(symbol=symbol, leverage=lev)
                print(f"  ✅ Set to {lev}x: {result}")
                break
            except Exception as e:
                print(f"  ❌ {lev}x failed: {str(e)[:100]}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "="*60)
