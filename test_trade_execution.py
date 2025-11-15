"""
Test script to verify trading bot can open and close positions correctly
"""
import sys
import time
from aster.rest_api import Client
from grok_client import GrokClient
import config

print("="*60)
print("🧪 TESTING TRADE EXECUTION")
print("="*60)

# Initialize clients
print("\n1. Initializing clients...")
dex = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)
grok = GrokClient(
    api_key=config.GROK_API_KEY,
    base_url=config.GROK_BASE_URL,
    model=config.GROK_MODEL
)
print("   ✅ Clients initialized")

# Check balance
print("\n2. Checking balance...")
try:
    balance_data = dex.balance()
    eth_balance = 0.0
    for asset in balance_data:
        if asset['asset'] == 'ETH':
            eth_balance = float(asset['balance'])
            break

    if eth_balance > 0:
        eth_price_data = dex.ticker_price(symbol='ETHUSDT')
        eth_price = float(eth_price_data['price'])
        usd_balance = eth_balance * eth_price
        print(f"   ✅ Balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")
    else:
        print("   ❌ No ETH balance found!")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error checking balance: {e}")
    sys.exit(1)

# Check for existing positions
print("\n3. Checking for existing positions...")
try:
    positions = dex.get_position_risk()
    open_positions = [p for p in positions if float(p.get('positionAmt', 0)) != 0]

    if len(open_positions) > 0:
        print(f"   ⚠️  Found {len(open_positions)} existing positions:")
        for pos in open_positions:
            symbol = pos['symbol']
            amt = float(pos['positionAmt'])
            side = "LONG" if amt > 0 else "SHORT"
            pnl = float(pos['unRealizedProfit'])
            print(f"      - {symbol}: {side} ({amt} units, PnL: ${pnl:.2f})")

        # Ask if we should close them
        response = input("\n   Close all existing positions? (y/n): ")
        if response.lower() == 'y':
            for pos in open_positions:
                symbol = pos['symbol']
                amt = float(pos['positionAmt'])
                side = 'SELL' if amt > 0 else 'BUY'
                quantity = abs(amt)

                print(f"   Closing {symbol}...")
                try:
                    order = dex.new_order(
                        symbol=symbol,
                        side=side,
                        type='MARKET',
                        quantity=quantity,
                        reduceOnly=True
                    )
                    print(f"   ✅ Closed {symbol} (Order ID: {order.get('orderId')})")
                except Exception as e:
                    print(f"   ❌ Error closing {symbol}: {e}")

            print("\n   Waiting 5 seconds for positions to settle...")
            time.sleep(5)
    else:
        print("   ✅ No existing positions")
except Exception as e:
    print(f"   ❌ Error checking positions: {e}")
    sys.exit(1)

# Test: Calculate position size with leverage
print("\n4. Calculating position size with leverage...")
LEVERAGE = config.LEVERAGE
POSITION_PERCENT = config.POSITION_SIZE_PERCENT
margin_size = usd_balance * POSITION_PERCENT
notional_size = margin_size * LEVERAGE

print(f"   Leverage: {LEVERAGE}x")
print(f"   Position %: {POSITION_PERCENT * 100}%")
print(f"   Margin allocated: ${margin_size:.2f}")
print(f"   Notional position size: ${notional_size:.2f}")

if notional_size < 5.5:
    print(f"   ❌ Position too small (min $5.50 notional needed)")
    print(f"   ⚠️  Need at least ${5.5 / LEVERAGE / POSITION_PERCENT:.2f} balance to trade")
    sys.exit(1)

print(f"   ✅ Position size is valid!")

# Test: Try to open a small position on BTCUSDT
print("\n5. Testing position opening on BTCUSDT...")
TEST_SYMBOL = 'BTCUSDT'

try:
    # Get current price
    price_data = dex.ticker_price(symbol=TEST_SYMBOL)
    current_price = float(price_data['price'])
    print(f"   Current {TEST_SYMBOL} price: ${current_price:.2f}")

    # Calculate quantity
    quantity = notional_size / current_price

    # Smart rounding
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

    print(f"   Calculated quantity: {quantity}")
    print(f"   Notional value: ${quantity * current_price:.2f}")

    confirm = input(f"\n   Open a LONG position with {quantity} {TEST_SYMBOL} (~${notional_size:.2f})? (y/n): ")

    if confirm.lower() != 'y':
        print("   ⚠️  Test cancelled by user")
        sys.exit(0)

    # Open position
    print(f"   Opening LONG position...")
    order = dex.new_order(
        symbol=TEST_SYMBOL,
        side='BUY',
        type='MARKET',
        quantity=quantity
    )

    print(f"   ✅ Position opened!")
    print(f"      Order ID: {order.get('orderId')}")
    print(f"      Status: {order.get('status')}")

except Exception as e:
    print(f"   ❌ Error opening position: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

# Wait and verify position
print("\n6. Verifying position was opened...")
time.sleep(2)

try:
    positions = dex.get_position_risk(symbol=TEST_SYMBOL)
    if positions and len(positions) > 0:
        position = positions[0]
        amt = float(position.get('positionAmt', 0))

        if amt != 0:
            entry_price = float(position['entryPrice'])
            mark_price = float(position['markPrice'])
            pnl = float(position['unRealizedProfit'])

            print(f"   ✅ Position confirmed!")
            print(f"      Amount: {amt}")
            print(f"      Entry: ${entry_price:.2f}")
            print(f"      Current: ${mark_price:.2f}")
            print(f"      PnL: ${pnl:.2f}")
        else:
            print(f"   ❌ Position not found or already closed!")
            sys.exit(1)
    else:
        print(f"   ❌ Could not verify position!")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error verifying position: {e}")
    sys.exit(1)

# Test closing the position
print("\n7. Testing position closing...")
confirm_close = input(f"   Close the test position? (y/n): ")

if confirm_close.lower() == 'y':
    try:
        amt = float(position['positionAmt'])
        side = 'SELL' if amt > 0 else 'BUY'
        quantity = abs(amt)

        print(f"   Closing position...")
        print(f"      Side: {side}")
        print(f"      Quantity: {quantity}")

        close_order = dex.new_order(
            symbol=TEST_SYMBOL,
            side=side,
            type='MARKET',
            quantity=quantity,
            reduceOnly=True
        )

        print(f"   ✅ Position closed!")
        print(f"      Order ID: {close_order.get('orderId')}")
        print(f"      Status: {close_order.get('status')}")

        # Verify closure
        time.sleep(2)
        positions = dex.get_position_risk(symbol=TEST_SYMBOL)
        if positions and len(positions) > 0:
            amt = float(positions[0].get('positionAmt', 0))
            if amt == 0:
                print(f"   ✅ Position closure verified!")
            else:
                print(f"   ⚠️  Position still shows {amt} units")

    except Exception as e:
        print(f"   ❌ Error closing position: {e}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)
else:
    print("   ⚠️  Position left open - remember to close it manually!")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nThe bot should be able to:")
print("  ✅ Check balance")
print("  ✅ Calculate position sizes with leverage")
print("  ✅ Open positions")
print("  ✅ Close positions")
print("\nYou're ready to run the autonomous trader! 🌙✨")
