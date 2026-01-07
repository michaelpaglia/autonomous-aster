"""
Configuration module - loads settings from environment variables.
Copy .env.example to .env and fill in your values.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AsterDEX API Configuration
ASTERDEX_BASE_URL = os.getenv("ASTERDEX_BASE_URL", "https://fapi.asterdex.com")
ASTERDEX_MAIN_WALLET = os.getenv("ASTERDEX_MAIN_WALLET", "")
ASTERDEX_API_WALLET = os.getenv("ASTERDEX_API_WALLET", "")
ASTERDEX_PRIVATE_KEY = os.getenv("ASTERDEX_PRIVATE_KEY", "")
ASTERDEX_API_KEY = os.getenv("ASTERDEX_API_KEY", "")
ASTERDEX_API_SECRET = os.getenv("ASTERDEX_API_SECRET", "")

# xAI Grok Configuration
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
GROK_BASE_URL = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4-fast-non-reasoning")

# Trading Configuration
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))
USE_ALL_SYMBOLS = os.getenv("USE_ALL_SYMBOLS", "True").lower() == "true"
POSITION_SIZE_PERCENT = float(os.getenv("POSITION_SIZE_PERCENT", "0.85"))
MIN_BALANCE_USD = float(os.getenv("MIN_BALANCE_USD", "1"))
MIN_POSITION_NOTIONAL = float(os.getenv("MIN_POSITION_NOTIONAL", "5.5"))
MAX_OPEN_POSITIONS = int(os.getenv("MAX_OPEN_POSITIONS", "3"))
LEVERAGE_MIN = int(os.getenv("LEVERAGE_MIN", "10"))
LEVERAGE_MAX = int(os.getenv("LEVERAGE_MAX", "20"))

# Manual symbol list (only used if USE_ALL_SYMBOLS = False)
TRADING_SYMBOLS = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
]
