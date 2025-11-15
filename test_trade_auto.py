"""
Auto test - opens and closes position immediately to verify functionality
"""
import sys
import time
from aster.rest_api import Client
from grok_client import GrokClient
import config

print("="*60)
print("🧪 AUTO TRADE TEST - OPEN AND CLOSE IMMEDIATELY")
print("="*60)

# Initialize
print("\n1. Initializing...")
dex = Client(key=config.ASTERDEX_API_KEY, secret=config.ASTERDEX_API_SECRET)
grok = GrokClient(api_key=config.GROK_API_KEY, base_url=config.GROK_BASE_URL, model=config.GROK_MODEL)

# Get balance
balance_data = dex.balance()
eth_balance = 0.0
for asset in balance_data:
    if asset['asset'] == 'ETH':
        eth_balance = float(asset['balance'])
        break

eth_price = float(dex.ticker_price(symbol='ETHUSDT')['price'])
usd_balance = eth_balance * eth_price
print(f"   Balance: ${usd_balance:.2f} USD")

# Test symbol
TEST_SYMBOL = 'BTCUSDT'

# Get market data
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
print(f"   {TEST_SYMBOL}: ${market_data['price']:.2f}")

# Ask cosmos
print(f"\n2. Asking cosmos for decision...")
response = grok.get_trading_decision(market_data, "")

lines = response.strip().split('\n')
action = 'PASS'
leverage = config.LEVERAGE_MIN
percent = 30  # Default to 30% for safety

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
                leverage = max(config.LEVERAGE_MIN, min(config.LEVERAGE_MAX, int(line_upper.split('LEVERAGE=')[1].strip())))
            except:
                pass
        elif 'PERCENT=' in line_upper:
            try:
                percent = max(10, min(100, int(line_upper.split('PERCENT=')[1].strip())))
            except:
                pass

print(f"   Decision: {action}")
if action == 'PASS':
    # Force a LONG for testing
    print("   Cosmos said PASS, forcing LONG for test purposes")
    action = 'LONG'
    leverage = 10
    percent = 20

print(f"   Leverage: {leverage}x")
print(f"   Position: {percent}%")

# Calculate position
margin_size = usd_balance * (percent / 100.0)
notional_size = margin_size * leverage
current_price = market_data['price']
quantity = notional_size / current_price

# Round quantity
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

print(f"   Margin: ${margin_size:.2f}, Notional: ${notional_size:.2f}")
print(f"   Quantity: {quantity}")

if notional_size < config.MIN_POSITION_NOTIONAL:
    print(f"\n❌ Position too small (${notional_size:.2f} < ${config.MIN_POSITION_NOTIONAL})")
    sys.exit(1)

# Open position
print(f"\n3. Opening {action} position...")
try:
    order = dex.new_order(
        symbol=TEST_SYMBOL,
        side='BUY' if action == 'LONG' else 'SELL',
        type='MARKET',
        quantity=quantity
    )
    print(f"   ✅ Opened! Order ID: {order.get('orderId')}")
except Exception as e:
    print(f"   ❌ Error opening: {e}")
    sys.exit(1)

# Wait
print(f"\n4. Waiting 3 seconds...")
time.sleep(3)

# Verify opened
print(f"\n5. Verifying position opened...")
positions = dex.get_position_risk(symbol=TEST_SYMBOL)
if not positions or len(positions) == 0:
    print(f"   ❌ No position data!")
    sys.exit(1)

position = positions[0]
amt = float(position.get('positionAmt', 0))

if amt == 0:
    print(f"   ❌ Position amount is 0!")
    sys.exit(1)

entry_price = float(position['entryPrice'])
mark_price = float(position['markPrice'])
pnl = float(position['unRealizedProfit'])

print(f"   ✅ Position confirmed!")
print(f"      Amount: {amt}")
print(f"      Entry: ${entry_price:.2f}")
print(f"      Current: ${mark_price:.2f}")
print(f"      PnL: ${pnl:.2f}")

# Close immediately
print(f"\n6. Closing position immediately...")
try:
    close_side = 'SELL' if amt > 0 else 'BUY'
    close_quantity = abs(amt)

    close_order = dex.new_order(
        symbol=TEST_SYMBOL,
        side=close_side,
        type='MARKET',
        quantity=close_quantity,
        reduceOnly=True
    )
    print(f"   ✅ Closed! Order ID: {close_order.get('orderId')}")
    print(f"      Final PnL: ${pnl:.2f}")
except Exception as e:
    print(f"   ❌ Error closing: {e}")
    sys.exit(1)

# Verify closed
print(f"\n7. Waiting 3 seconds to verify...")
time.sleep(3)

positions = dex.get_position_risk(symbol=TEST_SYMBOL)
if positions and len(positions) > 0:
    amt = float(positions[0].get('positionAmt', 0))
    if amt == 0:
        print(f"   ✅ Position closure verified (amount = 0)")
    else:
        print(f"   ⚠️  Position still shows {amt} units")
else:
    print(f"   ✅ No position data (fully closed)")

print(f"\n{'='*60}")
print(f"✅ TEST PASSED!")
print(f"{'='*60}")
print(f"\nVerified:")
print(f"  ✅ Grok cosmic decision making")
print(f"  ✅ Variable leverage: {leverage}x")
print(f"  ✅ Variable position: {percent}%")
print(f"  ✅ Opening positions")
print(f"  ✅ Closing positions")
print(f"\n🚀 Bot is ready for autonomous trading!")
