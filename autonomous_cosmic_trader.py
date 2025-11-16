"""
🌙 ✨ AUTONOMOUS COSMIC TRADER ✨ 🌙
24/7 Astrology-Based Trading Bot

This bot runs continuously and makes trading decisions based purely on:
- Cosmic vibes and astrological alignments
- Moon phases and planetary movements
- Spiritual energy and gut feelings

NO technical analysis. NO fundamentals. ONLY VIBES.
"""
import time
import logging
from datetime import datetime
from aster.rest_api import Client
from grok_client import GrokClient
from stats_exporter import StatsExporter
import config
import json
import sys
import traceback
import random

# Setup logging with Windows-compatible encoding
import platform

# Configure file handler (UTF-8 for emojis)
file_handler = logging.FileHandler('cosmic_trader.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Configure console handler (ASCII-safe for Windows)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# On Windows, use ASCII-only format; on Unix, allow emojis
if platform.system() == 'Windows':
    # Windows-safe format without emojis
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
else:
    # Unix can handle emojis
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Windows emoji compatibility
IS_WINDOWS = platform.system() == 'Windows'

class SafeLogger:
    """Logger wrapper that strips emojis on Windows"""
    def __init__(self, logger):
        self._logger = logger

    def _clean(self, msg):
        if IS_WINDOWS and isinstance(msg, str):
            # Remove emojis on Windows to prevent encoding errors
            import re
            # Remove all emoji characters
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub('', msg)
        return msg

    def info(self, msg, *args, **kwargs):
        self._logger.info(self._clean(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(self._clean(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(self._clean(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(self._clean(msg), *args, **kwargs)

# Wrap logger for Windows compatibility
logger = SafeLogger(logger)


class AutonomousCosmicTrader:
    def __init__(self):
        """Initialize the autonomous cosmic trader"""
        logger.info("🌙 Initializing Autonomous Cosmic Trader...")

        self.dex = Client(
            key=config.ASTERDEX_API_KEY,
            secret=config.ASTERDEX_API_SECRET
        )

        self.grok = GrokClient(
            api_key=config.GROK_API_KEY,
            base_url=config.GROK_BASE_URL,
            model=config.GROK_MODEL
        )

        # Stats exporter for dashboard
        self.stats = StatsExporter(self.dex)

        # Trading configuration
        self.CHECK_INTERVAL = config.CHECK_INTERVAL_MINUTES * 60  # Convert to seconds
        self.MAX_POSITIONS = config.MAX_OPEN_POSITIONS
        self.MIN_BALANCE_USD = config.MIN_BALANCE_USD
        self.LEVERAGE_MIN = config.LEVERAGE_MIN
        self.LEVERAGE_MAX = config.LEVERAGE_MAX
        self.MIN_POSITION_NOTIONAL = config.MIN_POSITION_NOTIONAL

        # Load trading symbols
        if config.USE_ALL_SYMBOLS:
            logger.info("🌟 Loading ALL available symbols from exchange...")
            self.SYMBOLS = self._fetch_all_symbols()
            logger.info(f"✓ Loaded {len(self.SYMBOLS)} cosmic trading symbols!")
        else:
            self.SYMBOLS = config.TRADING_SYMBOLS
            logger.info(f"✓ Using manual symbol list: {len(self.SYMBOLS)} symbols")

        # Balance tracking
        self.last_balance = 0.0
        self.current_position_size_usd = 0.0

        logger.info(f"✓ Connected to cosmic realm")
        logger.info(f"✓ Leverage range: {self.LEVERAGE_MIN}-{self.LEVERAGE_MAX}x (cosmos decides!)")
        logger.info(f"✓ Position sizing: 10-100% of balance (cosmos decides!)")
        logger.info(f"✓ Max positions: {self.MAX_POSITIONS}")
        logger.info(f"✓ Check interval: {config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"✓ Min balance threshold: ${self.MIN_BALANCE_USD}")

    def _fetch_all_symbols(self):
        """Fetch all available trading symbols from exchange"""
        try:
            exchange_info = self.dex.exchange_info()
            symbols = exchange_info.get('symbols', [])

            # Filter to only TRADING status and USDT pairs
            trading_symbols = [
                s.get('symbol') for s in symbols
                if s.get('status') == 'TRADING' and 'USDT' in s.get('symbol', '')
            ]

            return trading_symbols
        except Exception as e:
            logger.error(f"Error fetching symbols, using fallback list: {e}")
            return config.TRADING_SYMBOLS

    def get_balance(self):
        """Get available balance in ETH and USD equivalent"""
        try:
            balance_data = self.dex.balance()
            # Look for ETH balance (main trading asset)
            eth_balance = 0.0
            for asset in balance_data:
                if asset['asset'] == 'ETH':
                    eth_balance = float(asset['balance'])
                    break

            # Get ETH price to calculate USD value
            if eth_balance > 0:
                eth_price_data = self.dex.ticker_price(symbol='ETHUSDT')
                eth_price = float(eth_price_data['price'])
                usd_value = eth_balance * eth_price
                return eth_balance, usd_value

            return eth_balance, 0.0
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0.0, 0.0

    def check_and_adjust_for_balance_change(self):
        """Check for balance changes"""
        try:
            eth_balance, usd_balance = self.get_balance()

            # Detect balance changes
            if self.last_balance == 0.0:
                # First check
                self.last_balance = usd_balance
                logger.info(f"💰 Initial balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")
                logger.info(f"   Cosmos will decide position sizing on each trade!")
                return usd_balance

            balance_diff = usd_balance - self.last_balance

            if abs(balance_diff) > 1.0:  # Significant change (>$1)
                if balance_diff > 0:
                    logger.info(f"💰 🎉 DEPOSIT DETECTED! +${balance_diff:.2f}")
                    logger.info(f"   New balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")
                else:
                    logger.info(f"💰 ⚠️  WITHDRAWAL/LOSS DETECTED: ${balance_diff:.2f}")
                    logger.info(f"   New balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")

                self.last_balance = usd_balance

            return usd_balance

        except Exception as e:
            logger.error(f"Error checking balance change: {e}")
            return self.last_balance

    def get_open_positions(self):
        """Get all open positions"""
        try:
            positions = self.dex.get_position_risk()
            open_positions = [p for p in positions if float(p.get('positionAmt', 0)) != 0]
            return open_positions
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []

    def get_market_data(self, symbol):
        """Fetch market data for a symbol"""
        try:
            ticker = self.dex.ticker_24hr_price_change(symbol=symbol)
            price_data = self.dex.ticker_price(symbol=symbol)

            return {
                'symbol': symbol,
                'price': float(price_data['price']),
                'price_change_24h': float(ticker['priceChangePercent']),
                'high_24h': float(ticker['highPrice']),
                'low_24h': float(ticker['lowPrice']),
                'volume_24h': float(ticker['volume'])
            }
        except Exception as e:
            logger.error(f"Error fetching market data for {symbol}: {e}")
            return None

    def ask_cosmos(self, symbol, market_data):
        """Ask Grok for cosmic trading guidance with leverage and position size"""
        try:
            logger.info(f"🔮 Consulting the cosmos about {symbol}...")

            response = self.grok.get_trading_decision(market_data, "")

            # Parse response - extract action, leverage, and percent
            lines = response.strip().split('\n')
            action = 'PASS'
            leverage = self.LEVERAGE_MIN  # Default to min
            percent = 20  # Default to 20% if parsing fails

            # Parse first line for action
            if len(lines) > 0:
                first_line = lines[0].strip().upper()
                if 'LONG' in first_line and 'SHORT' not in first_line:
                    action = 'LONG'
                elif 'SHORT' in first_line:
                    action = 'SHORT'
                else:
                    action = 'PASS'

            # If not PASS, parse leverage and percent
            if action != 'PASS':
                for line in lines[1:]:
                    line_upper = line.upper().strip()
                    if 'LEVERAGE=' in line_upper:
                        try:
                            lev = int(line_upper.split('LEVERAGE=')[1].strip())
                            # Clamp to valid range
                            leverage = max(self.LEVERAGE_MIN, min(self.LEVERAGE_MAX, lev))
                        except:
                            pass
                    elif 'PERCENT=' in line_upper:
                        try:
                            pct = int(line_upper.split('PERCENT=')[1].strip())
                            # Clamp to valid range
                            percent = max(10, min(100, pct))
                        except:
                            pass

            logger.info(f"✨ Cosmic Decision: {action}")
            if action != 'PASS':
                logger.info(f"✨ Leverage: {leverage}x")
                logger.info(f"✨ Position Size: {percent}% of balance")
            logger.info(f"✨ Cosmic Reasoning: {response.strip()}")

            return action, leverage, percent, response.strip()

        except Exception as e:
            logger.error(f"Error consulting cosmos: {e}")
            return 'PASS', self.LEVERAGE_MIN, 20, "Cosmic connection disrupted"

    def check_exit_position(self, position):
        """Ask cosmos if we should exit a position - PURE VIBES ONLY"""
        try:
            symbol = position['symbol']
            entry_price = float(position['entryPrice'])
            current_price = float(position['markPrice'])
            position_amt = float(position['positionAmt'])
            side = "LONG" if position_amt > 0 else "SHORT"
            pnl = float(position['unRealizedProfit'])
            pnl_percent = (pnl / (abs(position_amt) * entry_price)) * 100

            logger.info(f"📊 Checking {side} position: {symbol} PnL: ${pnl:.2f} ({pnl_percent:.2f}%)")

            # NO stop-loss or take-profit logic! Only ask the cosmos!
            prompt = f"""
We have a {side} position on {symbol}:
Entry: ${entry_price}
Current: ${current_price}
PnL: ${pnl:.2f} ({pnl_percent:.2f}%)

Should we close this position?

Start with YES or NO, then explain the cosmic reasoning.
Ignore the profit/loss numbers - read the COSMIC ENERGY and planetary alignments!
"""

            response = self.grok.quick_decision(prompt)

            # Look for YES/NO at start of response
            response_upper = response.upper().strip()
            should_close = response_upper.startswith('YES')

            if should_close:
                logger.info(f"✨ Cosmos says CLOSE: {response}")
                return True, response
            else:
                logger.info(f"✨ Cosmos says HOLD: {response}")
                return False, response

        except Exception as e:
            logger.error(f"Error checking exit: {e}")
            return False, str(e)

    def close_position(self, symbol, reason):
        """Close a position with DETAILED validation"""
        try:
            logger.info("="*60)
            logger.info(f"🌙 ATTEMPTING TO CLOSE POSITION: {symbol}")
            logger.info(f"   Cosmic Reason: {reason}")

            # Get current position
            positions = self.dex.get_position_risk(symbol=symbol)
            logger.info(f"   Position data received: {len(positions)} position(s) found")

            position = positions[0] if positions else None

            if not position or float(position.get('positionAmt', 0)) == 0:
                logger.warning(f"❌ No open position found for {symbol}")
                logger.warning(f"   Position data: {position}")
                logger.info("="*60)
                return False

            position_amt = float(position['positionAmt'])
            entry_price = float(position['entryPrice'])
            mark_price = float(position['markPrice'])
            side = 'SELL' if position_amt > 0 else 'BUY'
            quantity = abs(position_amt)
            final_pnl = float(position.get('unRealizedProfit', 0))

            logger.info(f"   Position Amount: {position_amt}")
            logger.info(f"   Close Side: {side} (opposite of position)")
            logger.info(f"   Quantity to close: {quantity}")
            logger.info(f"   Entry Price: ${entry_price}")
            logger.info(f"   Current Price: ${mark_price}")

            # Place market order to close with reduceOnly=True
            logger.info(f"   Placing MARKET {side} order for {quantity} {symbol}...")
            order = self.dex.new_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity,
                reduceOnly=True  # This ensures we only close, not open new position
            )

            logger.info(f"   ✅ Order executed successfully!")
            logger.info(f"   Order ID: {order.get('orderId')}")
            logger.info(f"   Order Status: {order.get('status')}")

            # Big notification for position closed
            logger.info("")
            logger.info("🌙 ✨ POSITION CLOSED! ✨ 🌙")
            logger.info(f"   Symbol: {symbol}")
            logger.info(f"   Direction: {'LONG' if position_amt > 0 else 'SHORT'}")
            logger.info(f"   Quantity: {quantity}")
            logger.info(f"   Entry: ${entry_price}")
            logger.info(f"   Exit: ${mark_price}")
            logger.info(f"   PnL: ${final_pnl:.2f} {'🎉 TO THE MOON!' if final_pnl > 0 else '📉 The cosmos giveth and taketh'}")
            logger.info(f"   Cosmic Reason: {reason}")
            logger.info("="*60)

            return True

        except Exception as e:
            logger.error(f"❌ ERROR closing position {symbol}: {e}")
            logger.error(f"   Exception type: {type(e).__name__}")
            logger.error(f"   Full traceback:")
            logger.error(traceback.format_exc())
            logger.info("="*60)
            return False

    def open_position(self, symbol, side, leverage, position_percent, reason):
        """Open a new position with cosmic leverage and sizing"""
        try:
            # Check balance before opening position
            eth_balance, usd_balance = self.get_balance()

            if usd_balance < self.MIN_BALANCE_USD:
                logger.warning(f"⚠️  Insufficient balance: ${usd_balance:.2f} < ${self.MIN_BALANCE_USD} minimum")
                logger.warning(f"   Skipping trade. Please deposit more funds.")
                return False

            # Calculate position based on cosmos decision
            margin_size = usd_balance * (position_percent / 100.0)
            notional_size = margin_size * leverage

            # Auto-adjust if cosmos chose too much (with 20% buffer for safety)
            max_usable_balance = usd_balance * 0.80  # Leave 20% buffer
            if margin_size > max_usable_balance:
                old_percent = position_percent
                margin_size = max_usable_balance
                notional_size = margin_size * leverage
                position_percent = int((margin_size / usd_balance) * 100)
                logger.info(f"⚙️  Auto-adjusted: Cosmos wanted {old_percent}% but only {position_percent}% available")

            logger.info(f"🌟 Opening {side} position on {symbol}")
            logger.info(f"Cosmic Config:")
            logger.info(f"   Leverage: {leverage}x")
            logger.info(f"   Position %: {position_percent}%")
            logger.info(f"   Margin: ${margin_size:.2f}")
            logger.info(f"   Notional (with {leverage}x): ${notional_size:.2f}")
            logger.info(f"Balance: {eth_balance:.4f} ETH (${usd_balance:.2f})")

            # CRITICAL: Check minimum notional BEFORE trying to place order
            if notional_size < self.MIN_POSITION_NOTIONAL:
                logger.warning(f"⚠️  Position too small!")
                logger.warning(f"   Notional: ${notional_size:.2f} < Min: ${self.MIN_POSITION_NOTIONAL}")
                logger.warning(f"   Cosmos chose {position_percent}% with {leverage}x leverage")
                logger.warning(f"   Need higher % or leverage, or more balance")
                logger.warning(f"   Skipping {symbol} - looking for another opportunity...")
                return False

            # Check if we have enough balance for this trade
            # The margin_size IS what we're risking - make sure we actually have it
            # Add 20% buffer for fees, price movements, and safety
            required_balance = margin_size * 1.2

            if usd_balance < required_balance:
                logger.warning(f"⚠️  Insufficient balance for this position!")
                logger.warning(f"   Margin needed: ${margin_size:.2f}")
                logger.warning(f"   With 20% buffer: ${required_balance:.2f}")
                logger.warning(f"   Available: ${usd_balance:.2f}")
                logger.warning(f"   Cosmos chose {position_percent}% but we only have enough for ~{int((usd_balance/1.2)/usd_balance*100)}%")
                logger.warning(f"   Skipping {symbol}...")
                return False

            # Also check if the notional/leverage matches our margin expectation
            # (Sanity check - notional should equal margin * leverage)
            expected_notional = margin_size * leverage
            if abs(expected_notional - notional_size) > 0.01:
                logger.error(f"⚠️  Math error in calculation!")
                logger.error(f"   Expected notional: ${expected_notional:.2f}")
                logger.error(f"   Calculated notional: ${notional_size:.2f}")
                return False

            # Get current price
            market_data = self.get_market_data(symbol)
            if not market_data:
                logger.error(f"Could not fetch market data for {symbol}")
                return False

            current_price = market_data['price']

            # Calculate quantity based on notional size
            quantity = notional_size / current_price

            # Smart rounding based on quantity size
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

            logger.info(f"Quantity: {quantity} at ${current_price}")
            logger.info(f"Final notional: ${quantity * current_price:.2f}")

            # CRITICAL: Set leverage BEFORE placing order
            try:
                logger.info(f"   Setting leverage to {leverage}x for {symbol}...")
                lev_result = self.dex.change_leverage(symbol=symbol, leverage=leverage)
                logger.info(f"   ✅ Leverage set: {lev_result.get('leverage')}x (max notional: ${lev_result.get('maxNotionalValue')})")
            except Exception as e:
                # If leverage setting fails, try to find max allowed and use that
                error_msg = str(e)
                if 'leverage' in error_msg.lower() or 'exceeds' in error_msg.lower():
                    logger.warning(f"   ⚠️  {leverage}x not allowed for {symbol}, trying lower...")

                    # Try progressively lower leverage
                    for lower_lev in [15, 10, 5]:
                        if lower_lev < leverage:
                            try:
                                lev_result = self.dex.change_leverage(symbol=symbol, leverage=lower_lev)
                                leverage = lower_lev  # Update to what actually worked
                                # Recalculate notional with new leverage
                                notional_size = margin_size * leverage
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

                                logger.info(f"   ✅ Reduced to {leverage}x leverage")
                                logger.info(f"   Adjusted quantity: {quantity}")
                                break
                            except:
                                continue
                    else:
                        # Couldn't set any leverage
                        logger.error(f"   ❌ Could not set leverage for {symbol}")
                        logger.error(f"   Error: {error_msg}")
                        return False
                else:
                    logger.error(f"   ❌ Leverage error: {e}")
                    return False

            # Place market order
            order = self.dex.new_order(
                symbol=symbol,
                side='BUY' if side == 'LONG' else 'SELL',
                type='MARKET',
                quantity=quantity
            )

            # Big notification for position opened
            logger.info("="*60)
            logger.info(f"🚀 ✨ POSITION OPENED! ✨ 🚀")
            logger.info(f"   Symbol: {symbol}")
            logger.info(f"   Direction: {side}")
            logger.info(f"   Leverage: {leverage}x")
            logger.info(f"   Quantity: {quantity}")
            logger.info(f"   Price: ${current_price}")
            logger.info(f"   Margin: ${margin_size:.2f} ({position_percent}% of balance)")
            logger.info(f"   Notional: ${quantity * current_price:.2f}")
            logger.info(f"   Order ID: {order.get('orderId')}")
            logger.info(f"   Cosmic Reason: {reason}")
            logger.info("="*60)

            return True

        except Exception as e:
            logger.error(f"Error opening position {symbol}: {e}")
            logger.error(traceback.format_exc())
            return False

    def run_trading_cycle(self):
        """Execute one trading cycle"""
        try:
            logger.info("="*60)
            logger.info("🌙 Starting new trading cycle")
            logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("="*60)

            # Check for balance changes and adjust strategy
            usd_balance = self.check_and_adjust_for_balance_change()

            # Check minimum balance threshold
            if usd_balance < self.MIN_BALANCE_USD:
                logger.warning(f"⚠️  Balance ${usd_balance:.2f} below minimum ${self.MIN_BALANCE_USD}")
                logger.warning(f"   Pausing trading until balance increases")
                logger.warning(f"   Deposit more ETH at asterdex.com to resume trading")
                return

            # Get open positions
            open_positions = self.get_open_positions()
            logger.info(f"📊 Open Positions: {len(open_positions)}")

            # Check existing positions
            for position in open_positions:
                symbol = position['symbol']
                should_close, reason = self.check_exit_position(position)

                if should_close:
                    self.close_position(symbol, reason)
                    time.sleep(2)  # Wait between operations

            # Refresh positions after potential closes
            open_positions = self.get_open_positions()

            # Look for new opportunities if we have room
            if len(open_positions) < self.MAX_POSITIONS:
                logger.info(f"🔍 Scanning for cosmic opportunities...")

                # Randomize symbol order each cycle - cosmic chaos!
                symbols_to_check = self.SYMBOLS.copy()
                random.shuffle(symbols_to_check)
                logger.info(f"   Shuffled {len(symbols_to_check)} symbols for cosmic randomness")

                for symbol in symbols_to_check:
                    # Skip if we already have a position
                    if any(p['symbol'] == symbol for p in open_positions):
                        continue

                    # Get market data
                    market_data = self.get_market_data(symbol)
                    if not market_data:
                        continue

                    # Ask cosmos for action, leverage, and position size
                    action, leverage, percent, reason = self.ask_cosmos(symbol, market_data)

                    if action in ['LONG', 'SHORT']:
                        # Check if we still have room
                        open_positions = self.get_open_positions()
                        if len(open_positions) < self.MAX_POSITIONS:
                            # Try to open position - if it succeeds, stop looking
                            # If it fails (too small, insufficient balance, etc.), keep trying other symbols
                            success = self.open_position(symbol, action, leverage, percent, reason)
                            if success:
                                logger.info(f"✅ Successfully opened position on {symbol}!")
                                time.sleep(2)  # Wait between trades
                                break  # Only open one position per cycle
                            else:
                                logger.info(f"⚠️  Failed to open {symbol}, trying next symbol...")
                                # Continue to next symbol in the loop

                    time.sleep(1)  # Small delay between symbol checks

            # Export stats for dashboard
            logger.info("📊 Exporting stats to dashboard...")
            self.stats.export_stats()

            logger.info("🌙 Trading cycle complete")

        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
            logger.error(traceback.format_exc())

    def run(self):
        """Main loop - runs forever"""
        logger.info("="*60)
        logger.info("🌙 ✨ AUTONOMOUS COSMIC TRADER STARTED ✨ 🌙")
        logger.info("Trading based purely on astrology and vibes")
        logger.info("NO technical analysis. NO fundamentals. ONLY COSMIC ENERGY.")
        logger.info("="*60)

        while True:
            try:
                self.run_trading_cycle()

                # Wait until next check
                logger.info(f"😴 Resting... Next check in {config.CHECK_INTERVAL_MINUTES} minutes")
                logger.info("="*60)
                time.sleep(self.CHECK_INTERVAL)

            except KeyboardInterrupt:
                logger.info("\n🌙 Cosmic trader shutting down gracefully...")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                logger.error(traceback.format_exc())
                logger.info("😴 Sleeping 60 seconds before retry...")
                time.sleep(60)


if __name__ == "__main__":
    trader = AutonomousCosmicTrader()
    trader.run()
