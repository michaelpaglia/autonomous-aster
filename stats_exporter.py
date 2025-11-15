"""
Export trading stats to JSON for dashboard
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from aster.rest_api import Client
import config


class StatsExporter:
    def __init__(self, dex_client: Client):
        self.dex = dex_client
        self.stats_file = 'dashboard/public/stats.json'
        self.history_file = 'dashboard/public/history.json'

        # Ensure directory exists
        os.makedirs('dashboard/public', exist_ok=True)

        # Initialize history if not exists
        if not os.path.exists(self.history_file):
            self._save_json(self.history_file, [])

    def _save_json(self, filepath: str, data: Any):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_json(self, filepath: str) -> Any:
        """Load data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return []

    def get_balance_info(self) -> Dict[str, float]:
        """Get current balance"""
        try:
            balance_data = self.dex.balance()
            eth_balance = 0.0

            for asset in balance_data:
                if asset['asset'] == 'ETH':
                    eth_balance = float(asset['balance'])
                    break

            # Get ETH price
            if eth_balance > 0:
                eth_price_data = self.dex.ticker_price(symbol='ETHUSDT')
                eth_price = float(eth_price_data['price'])
                usd_value = eth_balance * eth_price
            else:
                eth_price = 0
                usd_value = 0

            return {
                'eth': eth_balance,
                'usd': usd_value,
                'eth_price': eth_price
            }
        except Exception as e:
            print(f"Error getting balance: {e}")
            return {'eth': 0, 'usd': 0, 'eth_price': 0}

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current open positions"""
        try:
            positions = self.dex.get_position_risk()
            open_positions = []

            for p in positions:
                position_amt = float(p.get('positionAmt', 0))
                if position_amt != 0:
                    entry_price = float(p.get('entryPrice', 0))
                    mark_price = float(p.get('markPrice', 0))
                    unrealized_pnl = float(p.get('unRealizedProfit', 0))

                    open_positions.append({
                        'symbol': p.get('symbol'),
                        'side': 'LONG' if position_amt > 0 else 'SHORT',
                        'quantity': abs(position_amt),
                        'entryPrice': entry_price,
                        'markPrice': mark_price,
                        'pnl': unrealized_pnl,
                        'pnlPercent': (unrealized_pnl / (abs(position_amt) * entry_price)) * 100 if entry_price > 0 else 0
                    })

            return open_positions
        except Exception as e:
            print(f"Error getting positions: {e}")
            return []

    def export_stats(self):
        """Export current stats and update history"""
        try:
            timestamp = datetime.now().isoformat()

            # Get current data
            balance = self.get_balance_info()
            positions = self.get_positions()

            # Calculate total PnL from positions
            total_pnl = sum(p['pnl'] for p in positions)

            # Current stats
            current_stats = {
                'timestamp': timestamp,
                'balance': balance,
                'positions': positions,
                'totalPnL': total_pnl,
                'openPositions': len(positions),
                'leverageRange': f"{config.LEVERAGE_MIN}-{config.LEVERAGE_MAX}x"
            }

            # Save current stats
            self._save_json(self.stats_file, current_stats)

            # Update history (keep last 24 hours of 10-min intervals = 144 points)
            history = self._load_json(self.history_file)
            history.append({
                'timestamp': timestamp,
                'balanceUsd': balance['usd'],
                'totalPnL': total_pnl,
                'openPositions': len(positions)
            })

            # Keep only last 144 data points (24 hours)
            if len(history) > 144:
                history = history[-144:]

            self._save_json(self.history_file, history)

            print(f"✅ Stats exported at {timestamp}")
            print(f"   Balance: ${balance['usd']:.2f}")
            print(f"   Open Positions: {len(positions)}")
            print(f"   Total PnL: ${total_pnl:.2f}")

            return current_stats

        except Exception as e:
            print(f"Error exporting stats: {e}")
            return None
