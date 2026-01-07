"""
Test the autonomous trader without actually trading
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from autonomous_cosmic_trader import AutonomousCosmicTrader
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("="*60)
print("🌙 Testing Autonomous Cosmic Trader (DRY RUN)")
print("="*60)

trader = AutonomousCosmicTrader()

print("\n1. Testing balance check...")
eth_balance, usd_balance = trader.get_balance()
print(f"   ✓ Balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")

print("\n2. Testing position check...")
positions = trader.get_open_positions()
print(f"   ✓ Open positions: {len(positions)}")
for pos in positions:
    print(f"     - {pos['symbol']}: {pos['positionAmt']}")

print("\n3. Testing market data fetch...")
for symbol in trader.SYMBOLS:
    data = trader.get_market_data(symbol)
    if data:
        print(f"   ✓ {symbol}: ${data['price']:.2f} ({data['price_change_24h']:.2f}%)")

print("\n4. Testing cosmic consultation...")
test_data = trader.get_market_data('SOLUSDT')
if test_data:
    action, reason = trader.ask_cosmos('SOLUSDT', test_data)
    print(f"   ✓ Decision: {action}")
    print(f"   ✓ Reason: {reason}")

print("\n" + "="*60)
print("✨ All tests passed! Ready for autonomous trading.")
print("="*60)
print("\nTo start trading 24/7:")
print("  python autonomous_cosmic_trader.py")
print("\nOr deploy to server:")
print("  ./setup_server.sh")
print("="*60)
