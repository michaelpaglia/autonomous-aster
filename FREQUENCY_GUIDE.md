# ⏰ Check Frequency Guide

## Why Frequent Checks Matter for Astrology Trading

**Cosmic energy shifts constantly!** Unlike traditional TA, astrological alignments and vibes can change rapidly:
- Moon phases transition
- Planetary aspects form and dissolve
- Cosmic energy ebbs and flows
- Spiritual vibrations fluctuate

**More frequent checks = More responsive to cosmic shifts!** 🌙✨

---

## ⚙️ Frequency Options

### 🚀 **Every 1 Minute** (Ultra Responsive)
```python
CHECK_INTERVAL_MINUTES = 1
```

**Pros:**
- ✅ Maximum cosmic sensitivity
- ✅ Catches fleeting astrological alignments
- ✅ Opens positions at perfect cosmic moments
- ✅ Exits quickly when vibes shift

**Cons:**
- ⚠️ Higher API costs (~$43/month)
- ⚠️ Many position checks
- ⚠️ May overreact to minor cosmic fluctuations

**Best for:** Aggressive trading, maximum cosmic attunement

---

### ⚡ **Every 5 Minutes** (Balanced - RECOMMENDED)
```python
CHECK_INTERVAL_MINUTES = 5
```

**Pros:**
- ✅ Very responsive to cosmic changes
- ✅ Catches most important alignments
- ✅ Reasonable API costs (~$9/month)
- ✅ Good balance of speed vs cost

**Cons:**
- ⚠️ Might miss very brief cosmic windows
- ⚠️ Moderate API usage

**Best for:** Most traders - great balance! ⭐

---

### 🌙 **Every 10-15 Minutes** (Moderate)
```python
CHECK_INTERVAL_MINUTES = 10  # or 15
```

**Pros:**
- ✅ Still catches major cosmic shifts
- ✅ Lower API costs (~$3-4/month)
- ✅ Less noisy decision-making

**Cons:**
- ⚠️ May miss quick cosmic opportunities
- ⚠️ Slower to react to vibe changes

**Best for:** Patient cosmic traders, budget-conscious

---

### 🐢 **Every 30+ Minutes** (Slow)
```python
CHECK_INTERVAL_MINUTES = 30  # or 60
```

**Pros:**
- ✅ Very low API costs (~$1.50/month)
- ✅ Only major cosmic events trigger trades

**Cons:**
- ⚠️ Misses many astrological alignments
- ⚠️ Slow to respond to cosmic shifts
- ⚠️ Could miss entire moon phase transitions

**Best for:** Long-term cosmic alignment trading only

---

## 💰 Cost Comparison

| Interval | API Calls/Day | API Cost/Month | Total w/ VPS |
|----------|---------------|----------------|--------------|
| 1 min | 1,440 | $43 | $48-53 |
| 5 min | 288 | $9 | $14-19 |
| 10 min | 144 | $4 | $9-14 |
| 15 min | 96 | $3 | $8-13 |
| 30 min | 48 | $1.50 | $6-12 |

*Assuming 3 symbols to check + position management*

---

## 🎯 Our Recommendation

**Start with 5 minutes** - perfect balance of:
- Fast cosmic responsiveness
- Reasonable costs (~$9/month)
- Catches most important alignments
- Not too noisy

**Can adjust anytime!** Just edit `config.py`:
```python
CHECK_INTERVAL_MINUTES = 5
```

Then restart:
```bash
sudo systemctl restart cosmic-trader
```

---

## 🌟 Advanced: Dynamic Frequency

**Future enhancement idea:** Bot could adjust frequency based on cosmic activity!

```python
# Hypothetical future feature
if mercury_in_retrograde:
    CHECK_INTERVAL_MINUTES = 1  # Check constantly!
elif full_moon_approaching:
    CHECK_INTERVAL_MINUTES = 5  # Increased sensitivity
else:
    CHECK_INTERVAL_MINUTES = 15  # Normal pace
```

For now, just set it to 5 minutes and let it ride! 🚀

---

## 📊 Real-World Examples

### **5-Minute Interval Day:**
```
00:00 - Check all positions, scan for new trades
00:05 - Check all positions, scan for new trades
00:10 - Cosmos says LONG SOL! Position opened 🚀
00:15 - Check positions (including new SOL)
00:20 - Check positions
00:25 - Cosmos says CLOSE BTC! Position closed 🌙
...
```

**Result:** 288 checks/day = Catches most cosmic opportunities!

### **30-Minute Interval Day:**
```
00:00 - Check all positions, scan for new trades
00:30 - Check all positions, scan for new trades
01:00 - Check all positions, scan for new trades
...
```

**Result:** 48 checks/day = Might miss short-lived cosmic windows

---

## ⚡ Making Changes

### To increase frequency:
```bash
# Edit config
nano config.py
# Change to: CHECK_INTERVAL_MINUTES = 1

# Restart bot
sudo systemctl restart cosmic-trader
```

### To decrease frequency:
```bash
# Edit config
nano config.py
# Change to: CHECK_INTERVAL_MINUTES = 30

# Restart bot
sudo systemctl restart cosmic-trader
```

**Takes effect immediately on restart!**

---

## 🌙 Bottom Line

**For pure astrology trading:**
- **Don't go slower than 10 minutes** - cosmic energy moves fast!
- **5 minutes is sweet spot** - responsive + affordable
- **1 minute if you're serious** - maximum cosmic attunement (costs more)

**Current default: 5 minutes** ⭐

The stars wait for no one! ⏰✨
