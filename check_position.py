"""
Check current SOL position
"""
from aster.rest_api import Client
import config
import json

client = Client(
    key=config.ASTERDEX_API_KEY,
    secret=config.ASTERDEX_API_SECRET
)

print("🌙 Checking your cosmic position...\n")

# Get SOL position
positions = client.get_position_risk(symbol='SOLUSDT')

for pos in positions:
    if float(pos.get('positionAmt', 0)) != 0:
        print("✨ ACTIVE POSITION FOUND! ✨\n")
        print(json.dumps(pos, indent=2))
        break
else:
    print("📊 Full position data:")
    print(json.dumps(positions, indent=2))
