"""
Quick test to verify autonomous trader can connect
Uses the same client as autonomous_cosmic_trader.py
"""
from aster.rest_api import Client
import config
import platform
import re

# Windows emoji compatibility
def clean_print(msg):
    """Remove emojis on Windows to prevent encoding errors"""
    if platform.system() == 'Windows':
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        msg = emoji_pattern.sub('', msg)
    print(msg)

clean_print("="*60)
clean_print("🌙 Testing Autonomous Cosmic Trader Connection 🌙")
clean_print("="*60)

try:
    clean_print("\n1. Creating AsterDEX client...")
    dex = Client(
        key=config.ASTERDEX_API_KEY,
        secret=config.ASTERDEX_API_SECRET
    )
    clean_print("   ✓ Client created")

    clean_print("\n2. Testing exchange info...")
    exchange_info = dex.exchange_info()
    symbols = exchange_info.get('symbols', [])
    clean_print(f"   ✓ Found {len(symbols)} trading symbols")

    clean_print("\n3. Testing balance...")
    balance_data = dex.balance()
    clean_print(f"   ✓ Balance retrieved: {len(balance_data)} assets")

    # Show ETH balance
    for asset in balance_data:
        if asset['asset'] == 'ETH':
            clean_print(f"   💰 ETH Balance: {asset['balance']}")
            break

    clean_print("\n4. Testing price data...")
    eth_price = dex.ticker_price(symbol='ETHUSDT')
    clean_print(f"   ✓ ETH Price: ${eth_price['price']}")

    clean_print("\n5. Testing positions...")
    positions = dex.get_position_risk()
    open_pos = [p for p in positions if float(p.get('positionAmt', 0)) != 0]
    clean_print(f"   ✓ Open positions: {len(open_pos)}")

    clean_print("\n" + "="*60)
    clean_print("✅ ALL TESTS PASSED!")
    clean_print("="*60)
    clean_print("\nYou're ready to run:")
    clean_print("  python autonomous_cosmic_trader.py")
    clean_print("\n🌙 May the cosmos guide your trades! 🌙")
    clean_print("="*60)

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
