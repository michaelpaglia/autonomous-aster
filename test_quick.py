"""
Quick test to verify autonomous trader can connect
Uses the same client as autonomous_cosmic_trader.py
"""
from aster.rest_api import Client
import config

print("="*60)
print("🌙 Testing Autonomous Cosmic Trader Connection 🌙")
print("="*60)

try:
    print("\n1. Creating AsterDEX client...")
    dex = Client(
        key=config.ASTERDEX_API_KEY,
        secret=config.ASTERDEX_API_SECRET
    )
    print("   ✓ Client created")

    print("\n2. Testing exchange info...")
    exchange_info = dex.exchange_info()
    symbols = exchange_info.get('symbols', [])
    print(f"   ✓ Found {len(symbols)} trading symbols")

    print("\n3. Testing balance...")
    balance_data = dex.balance()
    print(f"   ✓ Balance retrieved: {len(balance_data)} assets")

    # Show ETH balance
    for asset in balance_data:
        if asset['asset'] == 'ETH':
            print(f"   💰 ETH Balance: {asset['balance']}")
            break

    print("\n4. Testing price data...")
    eth_price = dex.ticker_price(symbol='ETHUSDT')
    print(f"   ✓ ETH Price: ${eth_price['price']}")

    print("\n5. Testing positions...")
    positions = dex.get_position_risk()
    open_pos = [p for p in positions if float(p.get('positionAmt', 0)) != 0]
    print(f"   ✓ Open positions: {len(open_pos)}")

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nYou're ready to run:")
    print("  python autonomous_cosmic_trader.py")
    print("\n🌙 May the cosmos guide your trades! 🌙")
    print("="*60)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure aster-connector is installed:")
    print("   pip install aster-connector-python")
    print("2. Check your config.py has:")
    print("   ASTERDEX_API_KEY = \"your_key_here\"")
    print("   ASTERDEX_API_SECRET = \"your_secret_here\"")
    print("\n" + "="*60)
    import traceback
    traceback.print_exc()
