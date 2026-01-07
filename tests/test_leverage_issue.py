"""
Quick test to reproduce leverage errors
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from aster.rest_api import Client
import config
import random
import time

print("Testing leverage issues...")

dex = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)

# Get balance
balance_data = dex.balance()
eth_balance = 0.0
for asset in balance_data:
    if asset['asset'] == 'ETH':
        eth_balance = float(asset['balance'])
        break

eth_price = float(dex.ticker_price(symbol='ETHUSDT')['price'])
usd_balance = eth_balance * eth_price

print(f"Balance: ${usd_balance:.2f}")

# Get some random symbols
exchange_info = dex.exchange_info()
symbols = [s['symbol'] for s in exchange_info['symbols'][:20] if s['status'] == 'TRADING']
random.shuffle(symbols)

print(f"\nTrying to place small test orders on random symbols with varying leverage...\n")

for symbol in symbols[:5]:
    try:
        # Get price
        ticker = dex.ticker_price(symbol=symbol)
        price = float(ticker['price'])

        # Try different leverage levels
        for leverage in [20, 15, 10, 5]:
            try:
                print(f"\n{symbol} at ${price:.4f}")

                # Try to set leverage first
                print(f"  Trying {leverage}x leverage...")
                result = dex.set_leverage(symbol=symbol, leverage=leverage)
                print(f"  ✅ Leverage set to {leverage}x")

                # Calculate tiny position
                margin = usd_balance * 0.10  # 10% of balance
                notional = margin * leverage
                quantity = notional / price

                # Round quantity
                if quantity >= 1:
                    quantity = round(quantity, 2)
                else:
                    quantity = round(quantity, 4)

                print(f"  Attempting order: {quantity} units, ${notional:.2f} notional")

                # Try to place order
                order = dex.new_order(
                    symbol=symbol,
                    side='BUY',
                    type='MARKET',
                    quantity=quantity
                )

                print(f"  ✅ ORDER PLACED! ID: {order.get('orderId')}")

                # Close it immediately
                time.sleep(2)
                close_order = dex.new_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=quantity,
                    reduceOnly=True
                )
                print(f"  ✅ ORDER CLOSED! ID: {close_order.get('orderId')}")

                # Success - move to next symbol
                break

            except Exception as e:
                error_msg = str(e)
                if 'leverage' in error_msg.lower():
                    print(f"  ❌ {leverage}x: {error_msg}")
                    # Try lower leverage
                    continue
                elif 'notional' in error_msg.lower():
                    print(f"  ❌ Position too small: {error_msg}")
                    break  # Try different symbol
                else:
                    print(f"  ❌ Other error: {error_msg}")
                    break

    except Exception as e:
        print(f"  ❌ Symbol error: {e}")
        continue

print("\n" + "="*60)
print("Test complete!")
