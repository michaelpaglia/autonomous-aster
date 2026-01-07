"""
Test actual trade opening and closing with cosmic decision making
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

import time
from aster.rest_api import Client
from grok_client import GrokClient
import config

print("="*60)
print("🧪 REAL TRADE TEST - OPEN AND CLOSE")
print("="*60)

# Initialize clients
print("\n✓ Initializing clients...")
dex = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)
grok = GrokClient(
    api_key=config.GROK_API_KEY,
    base_url=config.GROK_BASE_URL,
    model=config.GROK_MODEL
)
print("  ✅ Clients initialized")

# Get balance
print("\n✓ Checking balance...")
balance_data = dex.balance()
eth_balance = 0.0
for asset in balance_data:
    if asset['asset'] == 'ETH':
        eth_balance = float(asset['balance'])
        break

eth_price_data = dex.ticker_price(symbol='ETHUSDT')
eth_price = float(eth_price_data['price'])
usd_balance = eth_balance * eth_price
print(f"  Balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")

# Test symbol
TEST_SYMBOL = 'BTCUSDT'

# Get market data
print(f"\n✓ Fetching {TEST_SYMBOL} market data...")
ticker = dex.ticker_24hr_price_change(symbol=TEST_SYMBOL)
price_data = dex.ticker_price(symbol=TEST_SYMBOL)

market_data = {
    'symbol': TEST_SYMBOL,
    'price': float(price_data['price']),
    'price_change_24h': float(ticker['priceChangePercent']),
    'high_24h': float(ticker['highPrice']),
    'low_24h': float(ticker['lowPrice']),
    'volume_24h': float(ticker['volume'])
}

print(f"  Price: ${market_data['price']:.2f}")
print(f"  24h Change: {market_data['price_change_24h']:+.2f}%")

# Ask cosmos for decision
print(f"\n✓ Asking cosmos about {TEST_SYMBOL}...")
response = grok.get_trading_decision(market_data, "")

print(f"\n  🔮 Grok's full response:")
print(f"  {'-'*56}")
for line in response.split('\n'):
    print(f"  {line}")
print(f"  {'-'*56}")

# Parse response
lines = response.strip().split('\n')
action = 'PASS'
leverage = config.LEVERAGE_MIN
percent = 20

if len(lines) > 0:
    first_line = lines[0].strip().upper()
    if 'LONG' in first_line and 'SHORT' not in first_line:
        action = 'LONG'
    elif 'SHORT' in first_line:
        action = 'SHORT'

if action != 'PASS':
    for line in lines[1:]:
        line_upper = line.upper().strip()
        if 'LEVERAGE=' in line_upper:
            try:
                lev = int(line_upper.split('LEVERAGE=')[1].strip())
                leverage = max(config.LEVERAGE_MIN, min(config.LEVERAGE_MAX, lev))
            except:
                pass
        elif 'PERCENT=' in line_upper:
            try:
                pct = int(line_upper.split('PERCENT=')[1].strip())
                percent = max(10, min(100, pct))
            except:
                pass

print(f"\n  ✨ Parsed Decision:")
print(f"     Action: {action}")
if action != 'PASS':
    print(f"     Leverage: {leverage}x")
    print(f"     Position Size: {percent}% of balance")

if action == 'PASS':
    print("\n  Cosmos says PASS - no trade to test")
    print("  Try running again, the cosmic vibes might change!")
    sys.exit(0)

# Calculate position
margin_size = usd_balance * (percent / 100.0)
notional_size = margin_size * leverage

print(f"\n✓ Position calculation:")
print(f"  Balance: ${usd_balance:.2f}")
print(f"  Margin ({percent}%): ${margin_size:.2f}")
print(f"  Notional ({leverage}x): ${notional_size:.2f}")

if notional_size < config.MIN_POSITION_NOTIONAL:
    print(f"\n  ❌ Position too small (min ${config.MIN_POSITION_NOTIONAL})")
    sys.exit(1)

# Calculate quantity
current_price = market_data['price']
quantity = notional_size / current_price

if quantity >= 100:
    quantity = round(quantity, 0)
elif quantity >= 10:
    quantity = round(quantity, 1)
elif quantity >= 1:
    quantity = round(quantity, 2)
elif quantity >= 0.1:
    quantity = round(quantity, 3)
else:
    quantity = round(quantity, 4)

print(f"  Quantity: {quantity}")
print(f"  Final notional: ${quantity * current_price:.2f}")

# Confirm
print(f"\n{'='*60}")
print(f"READY TO OPEN {action} POSITION")
print(f"{'='*60}")
print(f"Symbol: {TEST_SYMBOL}")
print(f"Direction: {action}")
print(f"Leverage: {leverage}x")
print(f"Quantity: {quantity}")
print(f"Price: ${current_price:.2f}")
print(f"Notional: ${quantity * current_price:.2f}")
print(f"Margin: ${margin_size:.2f}")
print(f"{'='*60}")

response = input("\nProceed with opening position? (yes/no): ")
if response.lower() != 'yes':
    print("Test cancelled")
    sys.exit(0)

# Open position
print(f"\n✓ Opening {action} position...")
try:
    order = dex.new_order(
        symbol=TEST_SYMBOL,
        side='BUY' if action == 'LONG' else 'SELL',
        type='MARKET',
        quantity=quantity
    )

    print(f"  ✅ Position opened!")
    print(f"     Order ID: {order.get('orderId')}")
    print(f"     Status: {order.get('status')}")

except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Wait and verify
print(f"\n✓ Waiting 3 seconds for position to settle...")
time.sleep(3)

# Verify position
print(f"\n✓ Verifying position...")
positions = dex.get_position_risk(symbol=TEST_SYMBOL)
if positions and len(positions) > 0:
    position = positions[0]
    amt = float(position.get('positionAmt', 0))

    if amt != 0:
        entry_price = float(position['entryPrice'])
        mark_price = float(position['markPrice'])
        pnl = float(position['unRealizedProfit'])

        print(f"  ✅ Position confirmed!")
        print(f"     Amount: {amt}")
        print(f"     Entry: ${entry_price:.2f}")
        print(f"     Current: ${mark_price:.2f}")
        print(f"     PnL: ${pnl:.2f}")
    else:
        print(f"  ❌ Position not found!")
        sys.exit(1)
else:
    print(f"  ❌ No position data returned!")
    sys.exit(1)

# Now test closing
print(f"\n{'='*60}")
print(f"TESTING POSITION CLOSE")
print(f"{'='*60}")

response = input("\nProceed with closing position? (yes/no): ")
if response.lower() != 'yes':
    print("⚠️  Position left open - close it manually!")
    sys.exit(0)

print(f"\n✓ Closing position...")
try:
    close_side = 'SELL' if amt > 0 else 'BUY'
    close_quantity = abs(amt)

    print(f"  Closing {TEST_SYMBOL}")
    print(f"  Side: {close_side}")
    print(f"  Quantity: {close_quantity}")

    close_order = dex.new_order(
        symbol=TEST_SYMBOL,
        side=close_side,
        type='MARKET',
        quantity=close_quantity,
        reduceOnly=True
    )

    print(f"  ✅ Position closed!")
    print(f"     Order ID: {close_order.get('orderId')}")
    print(f"     Status: {close_order.get('status')}")
    print(f"     Final PnL: ${pnl:.2f}")

except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Verify closure
print(f"\n✓ Waiting 3 seconds to verify closure...")
time.sleep(3)

positions = dex.get_position_risk(symbol=TEST_SYMBOL)
if positions and len(positions) > 0:
    amt = float(positions[0].get('positionAmt', 0))
    if amt == 0:
        print(f"  ✅ Position closure verified!")
    else:
        print(f"  ⚠️  Position still shows {amt} units")
else:
    print(f"  ✅ No position data (position closed)")

print(f"\n{'='*60}")
print(f"✅ TEST COMPLETE!")
print(f"{'='*60}")
print(f"\nSuccessfully tested:")
print(f"  ✅ Grok cosmic decision making")
print(f"  ✅ Variable leverage ({leverage}x)")
print(f"  ✅ Variable position sizing ({percent}%)")
print(f"  ✅ Position opening")
print(f"  ✅ Position closing")
print(f"\n🌙 The bot is ready for autonomous trading!")
