"""
Quick test script to verify API connections
"""
from trading_bot import TradingBot


def main():
    print("="*60)
    print("Testing AsterDEX + Grok API Connections")
    print("="*60)

    bot = TradingBot()
    success = bot.test_connections()

    if success:
        print("\n✓ All API connections successful!")
        print("\nYou can now run: python trading_bot.py")
    else:
        print("\n✗ Connection tests failed")
        print("Please check your credentials in config.py")


if __name__ == "__main__":
    main()
