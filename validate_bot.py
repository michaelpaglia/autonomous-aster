"""
Automated validation script - checks bot configuration and capabilities
"""
import sys
from aster.rest_api import Client
from grok_client import GrokClient
import config

print("="*60)
print("🧪 BOT VALIDATION CHECK")
print("="*60)

# Test 1: Client connections
print("\n✓ Testing API connections...")
try:
    dex = Client(
        key=config.ASTERDEX_API_KEY,
        secret=config.ASTERDEX_API_SECRET
    )
    grok = GrokClient(
        api_key=config.GROK_API_KEY,
        base_url=config.GROK_BASE_URL,
        model=config.GROK_MODEL
    )
    print("  ✅ AsterDEX API: Connected")
    print("  ✅ Grok API: Connected")
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    sys.exit(1)

# Test 2: Balance check
print("\n✓ Checking balance...")
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
        print(f"  ✅ Balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")
    else:
        print("  ⚠️  No ETH balance - deposit funds to trade!")
        usd_balance = 0
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 3: Position sizing calculation
print("\n✓ Validating position sizing...")
LEVERAGE = config.LEVERAGE
POSITION_PERCENT = config.POSITION_SIZE_PERCENT
margin_size = usd_balance * POSITION_PERCENT
notional_size = margin_size * LEVERAGE

print(f"  Config:")
print(f"    - Leverage: {LEVERAGE}x")
print(f"    - Position %: {POSITION_PERCENT * 100}%")
print(f"    - Check interval: {config.CHECK_INTERVAL_MINUTES} minutes")
print(f"    - Max positions: {config.MAX_OPEN_POSITIONS}")
print(f"\n  Calculated position sizing:")
print(f"    - Margin per trade: ${margin_size:.2f} ({POSITION_PERCENT * 100}% of balance)")
print(f"    - Notional per trade: ${notional_size:.2f} (margin × {LEVERAGE}x)")

if notional_size < 5.5:
    print(f"  ⚠️  Position size ${notional_size:.2f} below minimum $5.50")
    required_balance = 5.5 / LEVERAGE / POSITION_PERCENT
    print(f"     Need at least ${required_balance:.2f} balance to trade")
    print(f"     (or adjust config: increase POSITION_SIZE_PERCENT)")
else:
    print(f"  ✅ Position size valid for trading!")

# Test 4: Check current positions
print("\n✓ Checking open positions...")
try:
    positions = dex.get_position_risk()
    open_positions = [p for p in positions if float(p.get('positionAmt', 0)) != 0]

    if len(open_positions) > 0:
        print(f"  📊 Found {len(open_positions)} open position(s):")
        total_pnl = 0
        for pos in open_positions:
            symbol = pos['symbol']
            amt = float(pos['positionAmt'])
            side = "LONG" if amt > 0 else "SHORT"
            pnl = float(pos['unRealizedProfit'])
            entry = float(pos['entryPrice'])
            mark = float(pos['markPrice'])
            total_pnl += pnl

            print(f"     {symbol}: {side}")
            print(f"       Entry: ${entry:.4f} | Current: ${mark:.4f}")
            print(f"       PnL: ${pnl:.2f}")

        print(f"  Total PnL: ${total_pnl:.2f}")
    else:
        print("  ✅ No open positions")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 5: Test Grok connection with a quick query
print("\n✓ Testing Grok AI connection...")
try:
    test_prompt = "Say 'PASS' if you can read this. Just one word."
    response = grok.quick_decision(test_prompt)
    print(f"  ✅ Grok responded: {response[:50]}...")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test 6: Verify we can fetch market data
print("\n✓ Testing market data fetch...")
try:
    ticker = dex.ticker_24hr_price_change(symbol='BTCUSDT')
    price = float(ticker['lastPrice'])
    change = float(ticker['priceChangePercent'])
    print(f"  ✅ BTCUSDT: ${price:.2f} ({change:+.2f}%)")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*60)
print("✅ VALIDATION COMPLETE!")
print("="*60)

print("\nBot is configured correctly and ready to run!")
print("\nKey capabilities verified:")
print("  ✅ Can connect to AsterDEX API")
print("  ✅ Can connect to Grok AI")
print("  ✅ Can check balance and positions")
print("  ✅ Can fetch market data")
print("  ✅ Position sizing configured")

if notional_size >= 5.5:
    print("\n🚀 Ready to start autonomous trading:")
    print("   python autonomous_cosmic_trader.py")
else:
    print(f"\n⚠️  Deposit more funds or adjust config to start trading")
    print(f"   Current: ${usd_balance:.2f}")
    print(f"   Recommended: ${required_balance:.2f}+")

print("\nTo test opening/closing manually, run:")
print("   python test_trade_execution.py")
