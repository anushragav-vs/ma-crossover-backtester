import pandas as pd
import matplotlib.pyplot as plt

# Load the full backtest results from CSV
df = pd.read_csv("data/GOOG_backtest_results.csv", index_col=0, parse_dates=True)

# We also need MA_20/MA_50 and signal columns - they're in the signals file
signals_df = pd.read_csv("data/GOOG_with_signals.csv", index_col=0, parse_dates=True)
df["MA_20"] = signals_df["MA_20"]
df["MA_50"] = signals_df["MA_50"]
df["Signal"] = signals_df["Signal"]

# Find the exact days a crossover happened (signal changed from 0 to 1 or 1 to 0)
df["signal_change"] = df["Signal"].diff()
buy_days = df[df["signal_change"] == 1]
sell_days = df[df["signal_change"] == -1]

# Calculate drawdown series for both strategy and buy and hold
df['strategy_drawdown'] = (df['strategy_equity'] / df['strategy_equity'].cummax()) - 1
df['buy_hold_drawdown'] = (df['buy_hold_equity'] / df['buy_hold_equity'].cummax()) - 1

# Build a 3-panel figure, sharing the same x-axis (date)
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# ---Panel 1: Price and Moving Averages with Buy/Sell Signals---
axes[0].plot(df.index, df["Close"], label="GOOG Price", color='black', linewidth=1)
axes[0].plot(df.index, df["MA_20"], label="MA 20", color='blue', alpha=0.8)
axes[0].plot(df.index, df["MA_50"], label="MA 50", color='orange', alpha=0.8)
axes[0].scatter(buy_days.index, buy_days["Close"], marker='^', color='green', s=60, label="Buy Signal", zorder=5)
axes[0].scatter(sell_days.index, sell_days["Close"], marker='v', color='red', s=60, label="Sell Signal", zorder=5)
axes[0].set_title("GOOG Price with MA Crossover Signals")
axes[0].set_ylabel("Price ($)")
axes[0].legend(loc="upper left")
axes[0].grid(True)

# ---Panel 2: Equity Curves---
axes[1].plot(df.index, df["strategy_equity"], label="MA Crossover Strategy", color='darkgreen')
axes[1].plot(df.index, df["buy_hold_equity"], label="Buy and Hold GOOG", color='blue', alpha=0.7)
axes[1].set_title("Growth of 1$")
axes[1].set_ylabel("Equity")
axes[1].legend(loc="upper left")
axes[1].grid(True)

# ---Panel 3: Drawdowns---
axes[2].fill_between(df.index, df['strategy_drawdown'], color='darkgreen', alpha=0.4, label="Strategy Drawdown")
axes[2].fill_between(df.index, df['buy_hold_drawdown'], color='blue', alpha=0.3, label="Buy and Hold Drawdown")
axes[2].set_title("Drawdowns Comparison")
axes[2].set_ylabel("Drawdown")
axes[2].set_xlabel("Date")
axes[2].legend(loc="lower left")
axes[2].grid(True)

plt.tight_layout
plt.savefig("images/full_strategy_report.png", dpi=150)
plt.show()
print("\nFull strategy report saved to images/full_strategy_report.png")