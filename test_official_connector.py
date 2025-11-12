"""
Test with official Aster connector
"""
from aster.rest_api import Client
import config
import json

print("="*60)
print("🌙 Testing Official Aster Connector 🌙")
print("="*60)

# Initialize client with API key and secret
client = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)

print("\n💰 Checking balance...\n")
try:
    balance = client.balance()
    print("Balance:")
    print(json.dumps(balance, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n📊 Checking positions...\n")
try:
    positions = client.get_position_risk()
    print("Positions:")
    print(json.dumps(positions, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n📈 Getting account info...\n")
try:
    account = client.account()
    print("Account:")
    print(json.dumps(account, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
