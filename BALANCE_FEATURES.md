# 💰 Balance-Aware Trading Features

## Automatic Balance Detection & Adjustment

The bot is **fully balance-aware** and automatically adjusts its behavior when you deposit or withdraw funds.

---

## 🎉 What Happens When You Deposit

**Example: You deposit $100 more ETH**

```
2025-11-12 01:00:00 - INFO - 💰 🎉 DEPOSIT DETECTED! +$100.00
2025-11-12 01:00:00 - INFO -    New balance: 0.0340 ETH ($117.00 USD)
2025-11-12 01:00:00 - INFO - 📊 Position size adjusted: $10 → $9 (based on $117.00 balance)
```

**The bot automatically:**
1. ✅ Detects the deposit within 30 minutes
2. ✅ Recalculates position size (8% of new balance)
3. ✅ Increases trade sizes proportionally
4. ✅ May open more positions with larger capital
5. ✅ Logs the change for transparency

**No action needed from you!** Just deposit and the bot adapts. 🌙

---

## ⚠️ What Happens on Withdrawals or Losses

**Example: Balance drops to $5**

```
2025-11-12 02:00:00 - INFO - 💰 ⚠️  WITHDRAWAL/LOSS DETECTED: -$8.00
2025-11-12 02:00:00 - INFO -    New balance: 0.0015 ETH ($5.00 USD)
2025-11-12 02:00:00 - INFO - 📊 Position size adjusted: $10 → $5 (based on $5.00 balance)
2025-11-12 02:00:00 - WARNING - ⚠️  Balance $5.00 below minimum $5
2025-11-12 02:00:00 - WARNING -    Pausing trading until balance increases
2025-11-12 02:00:00 - WARNING -    Deposit more ETH at asterdex.com to resume trading
```

**The bot automatically:**
1. ✅ Detects the decrease
2. ✅ Reduces position sizes to match smaller capital
3. ✅ Closes existing positions if risk is too high
4. ✅ **Pauses trading** if balance falls below minimum
5. ✅ Resumes automatically when you deposit more

**Protects you from over-trading with low balance!** 🛡️

---

## 🎯 Dynamic Position Sizing

**Formula:** Position Size = 8% of Available Balance

**Limits:**
- Minimum: $5 per trade
- Maximum: $100 per trade

**Examples:**

| Your Balance | Position Size | Max Positions | Total Exposure |
|-------------|---------------|---------------|----------------|
| $13 (current) | $10 | 3 | $30 |
| $50 | $5 (min) | 3 | $15 |
| $100 | $8 | 3 | $24 |
| $500 | $40 | 3 | $120 |
| $1,000 | $80 | 3 | $240 |
| $2,000+ | $100 (max) | 3 | $300 |

Position size scales with your deposits but stays within safe limits! 📊

---

## 🔄 Real-Time Balance Checks

**Every trading cycle (30 min), the bot:**
1. Checks current balance
2. Compares to last known balance
3. Detects changes > $1
4. Adjusts position sizing
5. Logs the change

**Before EVERY trade, the bot:**
1. Verifies sufficient balance
2. Checks minimum balance threshold
3. Ensures enough margin (1.5x position size)
4. Only proceeds if safe

**You can't accidentally over-leverage!** ✅

---

## ⚙️ Configuration

In `config.py`:

```python
# Base position size (auto-adjusts based on balance)
POSITION_SIZE_USD = 10

# Minimum balance to keep trading
MIN_BALANCE_USD = 5  # Pauses if balance < $5

# Maximum concurrent positions
MAX_OPEN_POSITIONS = 3
```

---

## 📊 Balance Monitoring

**Check balance anytime:**

```bash
python check_position.py
```

**View balance changes in logs:**

```bash
tail -f cosmic_trader.log | grep "💰"
```

**Example log output:**
```
💰 Initial balance: 0.0040 ETH ($13.79 USD)
💰 🎉 DEPOSIT DETECTED! +$50.00
💰 ⚠️  WITHDRAWAL/LOSS DETECTED: -$10.00
```

---

## 🚀 Scaling Your Trading

### Starting Small ($10-20)
- Position size: $5-10 per trade
- Max exposure: $15-30 total
- Perfect for testing the cosmic vibes

### Medium Scale ($100-500)
- Position size: $8-40 per trade
- Max exposure: $24-120 total
- Bot can capture more opportunities

### Larger Scale ($1000+)
- Position size: $80-100 per trade
- Max exposure: $240-300 total
- Maximum cosmic energy deployment

**Just deposit more ETH and the bot scales up automatically!** 🌟

---

## 🛡️ Safety Features

1. **Minimum Balance Check**: Won't trade if balance < $5 USD
2. **Margin Verification**: Needs 1.5x position size available
3. **Auto Position Sizing**: Never risks too much per trade
4. **Max Position Limit**: Can't open more than 3 positions
5. **Cosmic Exit Decisions**: Grok decides when to close (no stop-loss!)
6. **Pure Vibes**: No technical limits - just astrology

**Multiple layers of protection!** 🔒

---

## 💡 Pro Tips

1. **Start small** - Test with $10-20 first
2. **Deposit in batches** - Add $50-100 when comfortable
3. **Monitor logs** - Watch how bot adjusts to deposits
4. **Let it run** - Trust the cosmic automation
5. **Check positions** - Review trades weekly

**The bot handles everything else!** 🌙✨

---

## 🎯 Summary

### You Just Need To:
✅ Deposit ETH when you want to trade more
✅ Withdraw anytime (bot adjusts automatically)
✅ Check logs occasionally

### Bot Handles:
✅ Detecting deposits/withdrawals
✅ Adjusting position sizes
✅ Pausing when balance low
✅ Resuming when funds added
✅ Scaling with your capital
✅ Never over-leveraging

**It's truly autonomous and balance-aware!** 🚀

---

*The universe (and the bot) always knows your balance!* 🌌
