"""
Test balance check with correct wallet addresses
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from asterdex_client import AsterDEXClient
import config
import json

print("="*60)
print("🌙 Checking Your Cosmic Wallet Energy 🌙")
print("="*60)

dex = AsterDEXClient(
    base_url=config.ASTERDEX_BASE_URL,
    api_wallet=config.ASTERDEX_API_WALLET,
    private_key=config.ASTERDEX_PRIVATE_KEY,
    user_address=config.ASTERDEX_MAIN_WALLET
)

print(f"\n📍 Main Wallet: {config.ASTERDEX_MAIN_WALLET}")
print(f"📍 API Signer: {config.ASTERDEX_API_WALLET}\n")

print("💰 Fetching balance...\n")
try:
    balance = dex.get_balance()
    print("Balance:")
    print(json.dumps(balance, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n📊 Fetching positions...\n")
try:
    positions = dex.get_position_risk()
    print("Positions:")
    print(json.dumps(positions, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
