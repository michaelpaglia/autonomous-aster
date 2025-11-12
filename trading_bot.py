"""
AsterDEX Trading Bot with Grok AI Integration
Main script to coordinate trading operations
"""
import time
import json
from typing import Dict, Any, Optional
from asterdex_client import AsterDEXClient
from grok_client import GrokClient
import config


class TradingBot:
    def __init__(self):
        """Initialize trading bot with AsterDEX and Grok clients"""
        print("🌙 Initializing Cosmic Trading Bot...")

        # Initialize AsterDEX client
        self.dex_client = AsterDEXClient(
            base_url=config.ASTERDEX_BASE_URL,
            api_wallet=config.ASTERDEX_API_WALLET,
            private_key=config.ASTERDEX_PRIVATE_KEY,
            user_address=config.ASTERDEX_MAIN_WALLET
        )
        print("✓ Connected to the blockchain realm")

        # Initialize Grok client
        self.grok_client = GrokClient(
            api_key=config.GROK_API_KEY,
            base_url=config.GROK_BASE_URL,
            model=config.GROK_MODEL
        )
        print("✓ Channeling cosmic wisdom from Grok")

    def test_connections(self) -> bool:
        """Test connectivity to both APIs"""
        print("\n=== Testing API Connections ===\n")

        try:
            # Test AsterDEX connection
            print("Testing AsterDEX API...")
            ping_result = self.dex_client.ping()
            print(f"  Ping: {ping_result}")

            server_time = self.dex_client.get_server_time()
            print(f"  Server Time: {server_time}")

            exchange_info = self.dex_client.get_exchange_info()
            print(f"  Exchange Info: {len(exchange_info.get('symbols', []))} symbols available")

            print("✓ AsterDEX API connection successful\n")

        except Exception as e:
            print(f"✗ AsterDEX API connection failed: {e}\n")
            return False

        try:
            # Test Grok connection
            print("Testing Grok API...")
            test_response = self.grok_client.quick_decision("Say 'API connection successful' if you can read this.")
            print(f"  Response: {test_response}")
            print("✓ Grok API connection successful\n")

        except Exception as e:
            print(f"✗ Grok API connection failed: {e}\n")
            return False

        return True

    def get_account_summary(self) -> Dict[str, Any]:
        """Get account balance and positions"""
        print("\n=== Account Summary ===\n")

        try:
            balance = self.dex_client.get_balance()
            print("Balance:")
            print(json.dumps(balance, indent=2))

            positions = self.dex_client.get_position_risk()
            print("\nPositions:")
            print(json.dumps(positions, indent=2))

            return {
                'balance': balance,
                'positions': positions
            }

        except Exception as e:
            print(f"Error getting account summary: {e}")
            return {}

    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch comprehensive market data for a symbol"""
        print(f"\n=== Market Data for {symbol} ===\n")

        try:
            ticker = self.dex_client.get_ticker_24h(symbol)
            mark_price = self.dex_client.get_mark_price(symbol)
            order_book = self.dex_client.get_order_book(symbol, limit=20)

            market_data = {
                'symbol': symbol,
                'current_price': ticker.get('lastPrice'),
                'price_change_24h': ticker.get('priceChangePercent'),
                'high_24h': ticker.get('highPrice'),
                'low_24h': ticker.get('lowPrice'),
                'volume_24h': ticker.get('volume'),
                'mark_price': mark_price[0].get('markPrice') if isinstance(mark_price, list) else mark_price.get('markPrice'),
                'best_bid': order_book['bids'][0] if order_book.get('bids') else None,
                'best_ask': order_book['asks'][0] if order_book.get('asks') else None,
            }

            print(json.dumps(market_data, indent=2))
            return market_data

        except Exception as e:
            print(f"Error fetching market data: {e}")
            return {}

    def ask_grok(self, prompt: str, market_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Ask Grok for trading advice

        Args:
            prompt: Your question or instruction
            market_data: Optional market data to include in context

        Returns:
            Grok's response
        """
        print("\n=== 🔮 Channeling Cosmic Wisdom ===\n")
        print(f"Question: {prompt}\n")

        try:
            if market_data:
                response = self.grok_client.get_trading_decision(market_data, prompt)
            else:
                response = self.grok_client.quick_decision(prompt)

            print(f"✨ The Universe Says:\n{response}\n")
            return response

        except Exception as e:
            print(f"Error reading the cosmos: {e}")
            return ""

    def execute_trade(self, symbol: str, side: str, order_type: str = "MARKET",
                     quantity: Optional[float] = None, price: Optional[float] = None) -> Dict[str, Any]:
        """
        Execute a trade on AsterDEX

        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            order_type: 'MARKET', 'LIMIT', etc.
            quantity: Order quantity
            price: Price for limit orders

        Returns:
            Order result
        """
        print(f"\n=== Executing Trade ===")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}\n")

        try:
            result = self.dex_client.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )

            print("Order Result:")
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"Error executing trade: {e}")
            return {}

    def ai_trading_decision(self, symbol: str) -> None:
        """
        Get market data and ask Grok for a trading decision

        Args:
            symbol: Trading symbol to analyze
        """
        print(f"\n{'='*60}")
        print(f"🌙 Cosmic Vibe Check for {symbol}")
        print(f"{'='*60}")

        # Get market data
        market_data = self.get_market_data(symbol)

        if not market_data:
            print("The data streams are blocked... try again later")
            return

        # Ask Grok for analysis
        print("\n🔮 Reading the cosmic energy...\n")

        decision = self.ask_grok("", market_data)

        print("\n" + "="*60)


def main():
    """Main execution function"""
    print("="*60)
    print("🌙 ✨ ASTROLOGY CRYPTO TRADER ✨ 🌙")
    print("Trade on Vibes & Cosmic Energy Only")
    print("="*60)

    # Initialize bot
    bot = TradingBot()

    # Test connections
    if not bot.test_connections():
        print("The cosmic connection is blocked. Check your config.")
        return

    # Display menu
    while True:
        print("\n" + "="*60)
        print("🔮 COSMIC MENU 🔮")
        print("="*60)
        print("1. Test Cosmic Connections")
        print("2. Check Your Wallet Energy")
        print("3. Read Market Constellations")
        print("4. Ask the Universe")
        print("5. 🌙 Get Cosmic Trading Vibes 🌙")
        print("6. View Your Positions")
        print("7. Execute Trade (Advanced)")
        print("0. Return to the Physical Realm")
        print("="*60)

        choice = input("\nSelect option: ").strip()

        try:
            if choice == "0":
                print("\nExiting...")
                break

            elif choice == "1":
                bot.test_connections()

            elif choice == "2":
                bot.get_account_summary()

            elif choice == "3":
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                bot.get_market_data(symbol)

            elif choice == "4":
                prompt = input("Ask Grok: ").strip()
                bot.ask_grok(prompt)

            elif choice == "5":
                symbol = input("Enter symbol to analyze (e.g., BTCUSDT): ").strip().upper()
                bot.ai_trading_decision(symbol)

            elif choice == "6":
                positions = bot.dex_client.get_position_risk()
                print("\nOpen Positions:")
                print(json.dumps(positions, indent=2))

            elif choice == "7":
                print("\n⚠️  MANUAL TRADE - USE WITH CAUTION")
                symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Side (BUY/SELL): ").strip().upper()
                order_type = input("Order type (MARKET/LIMIT): ").strip().upper()
                quantity = float(input("Quantity: ").strip())
                price = None
                if order_type == "LIMIT":
                    price = float(input("Price: ").strip())

                confirm = input(f"\nConfirm {side} {quantity} {symbol} at {order_type}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    bot.execute_trade(symbol, side, order_type, quantity, price)
                else:
                    print("Trade cancelled")

            else:
                print("Invalid option")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
