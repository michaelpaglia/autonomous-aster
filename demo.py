"""
Quick demo of the trading bot functionality
"""
from trading_bot import TradingBot


def main():
    print("="*60)
    print("AsterDEX + Grok AI Trading Bot Demo")
    print("="*60)

    # Initialize bot
    bot = TradingBot()

    # Test connections
    print("\n1. Testing connections...")
    if not bot.test_connections():
        print("Connection failed. Exiting.")
        return

    # Get account summary
    print("\n2. Getting account summary...")
    bot.get_account_summary()

    # Get market data for BTC
    print("\n3. Fetching BTC market data...")
    market_data = bot.get_market_data("BTCUSDT")

    # Ask Grok for advice
    print("\n4. Asking Grok for trading advice...")
    bot.ask_grok("What are the key factors I should consider when trading BTC perpetual futures?")

    # AI trading decision
    print("\n5. Getting AI trading decision for BTC...")
    bot.ai_trading_decision("BTCUSDT")

    print("\n" + "="*60)
    print("Demo complete! You can now run: python trading_bot.py")
    print("="*60)


if __name__ == "__main__":
    main()
