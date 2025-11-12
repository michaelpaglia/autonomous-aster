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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cosmic_trader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


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
        self.SYMBOLS = config.TRADING_SYMBOLS
        self.BASE_POSITION_SIZE_USD = config.POSITION_SIZE_USD
        self.MAX_POSITIONS = config.MAX_OPEN_POSITIONS
        self.MIN_BALANCE_USD = config.MIN_BALANCE_USD

        # Balance tracking
        self.last_balance = 0.0
        self.current_position_size_usd = self.BASE_POSITION_SIZE_USD

        logger.info(f"✓ Connected to cosmic realm")
        logger.info(f"✓ Trading symbols: {self.SYMBOLS}")
        logger.info(f"✓ Base position size: ${self.BASE_POSITION_SIZE_USD}")
        logger.info(f"✓ Max positions: {self.MAX_POSITIONS}")
        logger.info(f"✓ Check interval: {config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"✓ Min balance threshold: ${self.MIN_BALANCE_USD}")

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
        """Dynamically adjust position size based on available balance"""
        # Scale position size with balance, but keep it reasonable
        # Use 5-10% of balance per position
        suggested_size = usd_balance * 0.08  # 8% of balance

        # Keep it between $5 and $100 per position
        suggested_size = max(5, min(100, suggested_size))

        # Round to nearest dollar
        suggested_size = round(suggested_size)

        if suggested_size != self.current_position_size_usd:
            old_size = self.current_position_size_usd
            self.current_position_size_usd = suggested_size
            logger.info(f"📊 Position size adjusted: ${old_size} → ${suggested_size} (based on ${usd_balance:.2f} balance)")

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

            # Parse response
            lines = response.strip().split('\n')
            decision = lines[0].strip().upper()
            reason = ' '.join(lines[1:]) if len(lines) > 1 else "The cosmos has spoken."

            # Extract decision
            if 'LONG' in decision:
                action = 'LONG'
            elif 'SHORT' in decision:
                action = 'SHORT'
            else:
                action = 'PASS'

            logger.info(f"✨ Cosmic Decision: {action}")
            logger.info(f"✨ Reason: {reason}")

            return action, reason

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

            logger.info(f"✅ Position closed: {symbol}")
            logger.info(f"Order ID: {order.get('orderId')}")

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

            # Check if we have enough for this position
            if usd_balance < self.current_position_size_usd * 1.5:  # Need 1.5x for margin
                logger.warning(f"⚠️  Balance too low for ${self.current_position_size_usd} position")
                logger.warning(f"   Available: ${usd_balance:.2f}, Need: ${self.current_position_size_usd * 1.5:.2f}")
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

            # Round to appropriate decimal places
            if symbol == 'BTCUSDT':
                quantity = round(quantity, 3)
            elif symbol == 'ETHUSDT':
                quantity = round(quantity, 2)
            else:
                quantity = round(quantity, 1)

            logger.info(f"Quantity: {quantity} at ${current_price}")

            # Place market order
            order = self.dex.new_order(
                symbol=symbol,
                side='BUY' if side == 'LONG' else 'SELL',
                type='MARKET',
                quantity=quantity
            )

            logger.info(f"✅ Position opened: {symbol} {side}")
            logger.info(f"Order ID: {order.get('orderId')}")

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
