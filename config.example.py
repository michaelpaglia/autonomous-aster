# AsterDEX API Configuration
ASTERDEX_BASE_URL = "https://fapi.asterdex.com"
ASTERDEX_MAIN_WALLET = "YOUR_MAIN_WALLET_ADDRESS"  # Main trading account
ASTERDEX_API_WALLET = "YOUR_API_WALLET_ADDRESS"  # API signer wallet
ASTERDEX_PRIVATE_KEY = "YOUR_PRIVATE_KEY"
ASTERDEX_API_KEY = "YOUR_API_KEY"
ASTERDEX_API_SECRET = "YOUR_API_SECRET"

# xAI Grok Configuration
GROK_API_KEY = "YOUR_GROK_API_KEY"
GROK_BASE_URL = "https://api.x.ai/v1"
GROK_MODEL = "grok-4-fast-non-reasoning"  # Fast non-reasoning model for quick trading decisions

# ============================================
# AUTONOMOUS TRADING CONFIGURATION
# ============================================

# Trading intervals (in minutes)
CHECK_INTERVAL_MINUTES = 5  # How often to check for new trades
                            # Cosmic energy changes fast! Check frequently.
                            # Options: 1, 5, 10, 15 minutes
                            # Lower = more responsive to cosmic shifts
                            # Note: More checks = slightly higher API costs (~$0.10/day at 5min)

# Symbol Selection
USE_ALL_SYMBOLS = True  # True = trade ALL 231 available symbols (cosmic abundance!)
                        # False = only trade symbols listed in TRADING_SYMBOLS below

# Manual symbol list (only used if USE_ALL_SYMBOLS = False)
TRADING_SYMBOLS = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
]

# Position sizing - PURE FLOW with balance
POSITION_SIZE_PERCENT = 0.85  # Use 85% of available balance per trade
                              # The universe adjusts our risk automatically!
                              # With $12 balance: 85% = $10.20 per trade
                              # With $100 balance: 85% = $85 per trade
                              # Go with the flow! 🌊

# Balance management
MIN_BALANCE_USD = 1  # Minimum balance to keep trading (in USD)
                     # Very low threshold - if we have funds, we trade!

# Risk management
MAX_OPEN_POSITIONS = 3  # Maximum number of concurrent positions

# NOTE: No stop-loss or take-profit! We go PURE VIBES ONLY! 🌙✨
# The cosmos (Grok) decides EVERYTHING based on astrology
# No technical limits, no safety nets - just trust the universe!
