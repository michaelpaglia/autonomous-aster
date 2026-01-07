#!/usr/bin/env python3
"""
Main entry point for the Autonomous Cosmic Trader.
Run this file to start the trading bot.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from autonomous_cosmic_trader import AutonomousCosmicTrader

if __name__ == "__main__":
    trader = AutonomousCosmicTrader()
    trader.run()
