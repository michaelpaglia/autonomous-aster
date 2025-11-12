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
import config
import json
import sys
import traceback

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

        # Trading configuration
        self.CHECK_INTERVAL = config.CHECK_INTERVAL_MINUTES * 60  # Convert to seconds
        self.MAX_POSITIONS = config.MAX_OPEN_POSITIONS
        self.MIN_BALANCE_USD = config.MIN_BALANCE_USD
        self.POSITION_SIZE_PERCENT = config.POSITION_SIZE_PERCENT

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
        logger.info(f"✓ Position sizing: {self.POSITION_SIZE_PERCENT * 100}% of balance")
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
        """Check for balance changes and adjust position sizing"""
        try:
            eth_balance, usd_balance = self.get_balance()

            # Detect balance changes
            if self.last_balance == 0.0:
                # First check
                self.last_balance = usd_balance
                logger.info(f"💰 Initial balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")
                # Adjust position size on first run too!
                self._adjust_position_size(usd_balance)
                return usd_balance

            balance_diff = usd_balance - self.last_balance

            if abs(balance_diff) > 1.0:  # Significant change (>$1)
                if balance_diff > 0:
                    logger.info(f"💰 🎉 DEPOSIT DETECTED! +${balance_diff:.2f}")
                    logger.info(f"   New balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")
                else:
                    logger.info(f"💰 ⚠️  WITHDRAWAL/LOSS DETECTED: ${balance_diff:.2f}")
                    logger.info(f"   New balance: {eth_balance:.4f} ETH (${usd_balance:.2f} USD)")

                # Adjust position sizing based on new balance
                self._adjust_position_size(usd_balance)

                self.last_balance = usd_balance

            return usd_balance

        except Exception as e:
            logger.error(f"Error checking balance change: {e}")
            return self.last_balance

    def _adjust_position_size(self, usd_balance):
        """Dynamically adjust position size based on available balance - PURE FLOW"""
        # Use configured percentage of balance
        suggested_size = usd_balance * self.POSITION_SIZE_PERCENT

        # AsterDEX requires minimum $5 per order, use $5.50 to ensure we're safely above after rounding
        MIN_ORDER_SIZE = 5.5
        if suggested_size < MIN_ORDER_SIZE and usd_balance >= MIN_ORDER_SIZE:
            # If we have enough balance but percentage is too low, use minimum
            suggested_size = MIN_ORDER_SIZE
            logger.info(f"WARNING: Position size would be ${usd_balance * self.POSITION_SIZE_PERCENT:.2f}, but using minimum ${MIN_ORDER_SIZE}")
        elif usd_balance < MIN_ORDER_SIZE:
            # Not enough balance for minimum order
            suggested_size = 0
            logger.warning(f"WARNING: Balance ${usd_balance:.2f} is below minimum order size ${MIN_ORDER_SIZE}")
        else:
            # Normal case - use percentage
            suggested_size = round(suggested_size, 2)

        if abs(suggested_size - self.current_position_size_usd) > 0.10:  # Changed if different by >$0.10
            old_size = self.current_position_size_usd
            self.current_position_size_usd = suggested_size
            if suggested_size > 0:
                logger.info(f"📊 Position size adjusted: ${old_size:.2f} → ${suggested_size:.2f} ({self.POSITION_SIZE_PERCENT * 100}% of ${usd_balance:.2f})")

        return suggested_size

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
        """Ask Grok for cosmic trading guidance"""
        try:
            logger.info(f"🔮 Consulting the cosmos about {symbol}...")

            prompt = f"""
            Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            Should I open a position on {symbol}?

            Respond ONLY with one of these exact formats:
            - "LONG" if cosmic energy says go long
            - "SHORT" if vibes say short
            - "PASS" if the universe says wait

            Then on a new line, give a brief mystical reason (1-2 sentences max).
            """

            response = self.grok.get_trading_decision(market_data, prompt)

            # Parse response - search entire response for decision keywords
            response_upper = response.upper()

            # Extract decision from anywhere in the response
            if 'LONG' in response_upper and 'SHORT' not in response_upper:
                action = 'LONG'
            elif 'SHORT' in response_upper:
                action = 'SHORT'
            else:
                action = 'PASS'

            logger.info(f"✨ Cosmic Decision: {action}")
            logger.info(f"✨ Reason: {response.strip()}")

            return action, response.strip()

        except Exception as e:
            logger.error(f"Error consulting cosmos: {e}")
            return 'PASS', "Cosmic connection disrupted"

    def check_exit_position(self, position):
        """Ask cosmos if we should exit a position - PURE VIBES ONLY"""
        try:
            symbol = position['symbol']
            entry_price = float(position['entryPrice'])
            current_price = float(position['markPrice'])
            position_amt = float(position['positionAmt'])
            pnl = float(position['unRealizedProfit'])
            pnl_percent = (pnl / (abs(position_amt) * entry_price)) * 100

            logger.info(f"📊 Checking position: {symbol} PnL: ${pnl:.2f} ({pnl_percent:.2f}%)")

            # NO stop-loss or take-profit logic! Only ask the cosmos!
            prompt = f"""
            We have a position on {symbol}:
            Entry: ${entry_price}
            Current: ${current_price}
            PnL: ${pnl:.2f} ({pnl_percent:.2f}%)

            What do the stars say? Should we CLOSE or HOLD?

            Ignore profit/loss numbers - just read the cosmic energy.
            Is the universe telling us to exit or stay?

            Be brief and mystical. Just say CLOSE or HOLD and a short cosmic reason.
            """

            response = self.grok.quick_decision(prompt)

            should_close = 'CLOSE' in response.upper()

            if should_close:
                logger.info(f"✨ Cosmos says: {response}")
                return True, response

            logger.info(f"✨ Holding based on vibes: {response}")
            return False, "Holding per cosmic guidance"

        except Exception as e:
            logger.error(f"Error checking exit: {e}")
            return False, str(e)

    def close_position(self, symbol, reason):
        """Close a position"""
        try:
            logger.info(f"🌙 Closing position on {symbol}. Reason: {reason}")

            # Get current position
            positions = self.dex.get_position_risk(symbol=symbol)
            position = positions[0] if positions else None

            if not position or float(position.get('positionAmt', 0)) == 0:
                logger.warning(f"No open position found for {symbol}")
                return False

            position_amt = float(position['positionAmt'])
            side = 'SELL' if position_amt > 0 else 'BUY'
            quantity = abs(position_amt)

            # Place market order to close
            order = self.dex.new_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity,
                reduceOnly=True
            )

            # Get final PnL
            final_pnl = float(position.get('unRealizedProfit', 0))

            # Big notification for position closed
            logger.info("="*60)
            logger.info(f"🌙 ✨ POSITION CLOSED! ✨ 🌙")
            logger.info(f"   Symbol: {symbol}")
            logger.info(f"   Side: {side}")
            logger.info(f"   Quantity: {quantity}")
            logger.info(f"   Entry: ${position['entryPrice']}")
            logger.info(f"   Exit: ${position['markPrice']}")
            logger.info(f"   PnL: ${final_pnl:.2f} {'🎉' if final_pnl > 0 else '📉'}")
            logger.info(f"   Reason: {reason}")
            logger.info(f"   Order ID: {order.get('orderId')}")
            logger.info("="*60)

            return True

        except Exception as e:
            logger.error(f"Error closing position {symbol}: {e}")
            return False

    def open_position(self, symbol, side, reason):
        """Open a new position"""
        try:
            # Check balance before opening position
            eth_balance, usd_balance = self.get_balance()

            if usd_balance < self.MIN_BALANCE_USD:
                logger.warning(f"⚠️  Insufficient balance: ${usd_balance:.2f} < ${self.MIN_BALANCE_USD} minimum")
                logger.warning(f"   Skipping trade. Please deposit more funds.")
                return False

            # Check if position size is valid (minimum $5.50 to ensure notional > $5 after rounding)
            if self.current_position_size_usd < 5.5:
                logger.warning(f"WARNING: Position size ${self.current_position_size_usd:.2f} is below minimum $5.50")
                logger.warning(f"   Skipping trade. Need more balance or higher position % in config.")
                return False

            # Check if we have enough for this position (need at least 2x for margin safety)
            if usd_balance < self.current_position_size_usd * 2:
                logger.warning(f"⚠️  Balance too low for ${self.current_position_size_usd:.2f} position")
                logger.warning(f"   Available: ${usd_balance:.2f}, Need: ${self.current_position_size_usd * 2:.2f}")
                return False

            logger.info(f"🌟 Opening {side} position on {symbol}")
            logger.info(f"Reason: {reason}")
            logger.info(f"Balance: {eth_balance:.4f} ETH (${usd_balance:.2f})")

            # Get current price
            market_data = self.get_market_data(symbol)
            if not market_data:
                logger.error(f"Could not fetch market data for {symbol}")
                return False

            current_price = market_data['price']

            # Calculate quantity based on CURRENT position size (adjusted for balance)
            quantity = self.current_position_size_usd / current_price

            # Smart rounding based on quantity size
            if quantity >= 100:
                quantity = round(quantity, 0)  # Round to whole numbers for large quantities
            elif quantity >= 10:
                quantity = round(quantity, 1)  # 1 decimal for medium quantities
            elif quantity >= 1:
                quantity = round(quantity, 2)  # 2 decimals for small quantities
            elif quantity >= 0.1:
                quantity = round(quantity, 3)  # 3 decimals for very small quantities
            else:
                quantity = round(quantity, 4)  # 4 decimals for tiny quantities

            logger.info(f"Quantity: {quantity} at ${current_price}")

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
            logger.info(f"   Quantity: {quantity}")
            logger.info(f"   Price: ${current_price}")
            logger.info(f"   Value: ${self.current_position_size_usd}")
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

                for symbol in self.SYMBOLS:
                    # Skip if we already have a position
                    if any(p['symbol'] == symbol for p in open_positions):
                        continue

                    # Get market data
                    market_data = self.get_market_data(symbol)
                    if not market_data:
                        continue

                    # Ask cosmos
                    action, reason = self.ask_cosmos(symbol, market_data)

                    if action in ['LONG', 'SHORT']:
                        # Check if we still have room
                        open_positions = self.get_open_positions()
                        if len(open_positions) < self.MAX_POSITIONS:
                            self.open_position(symbol, action, reason)
                            time.sleep(2)  # Wait between trades
                            break  # Only open one position per cycle

                    time.sleep(1)  # Small delay between symbol checks

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
