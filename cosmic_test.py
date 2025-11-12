"""
Quick test of the Cosmic Astrology Trader
"""
from trading_bot import TradingBot


def main():
    print("="*60)
    print("🌙 ✨ COSMIC VIBE CHECK ✨ 🌙")
    print("="*60)

    bot = TradingBot()

    print("\n🔮 Asking the universe about BTC...\n")

    # Get BTC market data
    market_data = bot.get_market_data("BTCUSDT")

    if market_data:
        print("\n🌙 Getting cosmic trading recommendation...\n")
        bot.ask_grok("", market_data)

    print("\n" + "="*60)
    print("✨ The cosmos has spoken ✨")
    print("="*60)


if __name__ == "__main__":
    main()
