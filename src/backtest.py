import pandas as pd
import matplotlib.pyplot as plt

# Load data with signals
df = pd.read_csv("data/GOOG_with_signals.csv", index_col=0, parse_dates=True)

#1. Daily stock returns(buy and hold return each day)
df["stock_return"] = df["Close"].pct_change()

#2. Strategy return = only earn the stocks return on days wrer in postion
df["strategy_return"] = df["position"] * df["stock_return"]

#3. Drop the first row where position/return is NaN(No signal yet)
df = df.dropna(subset=["strategy_return","stock_return"])

#4. Build equity curves (starting both at 1.0 = 100%)
df["strategy_equity"] = (1 + df["strategy_return"]).cumprod()
df["buy_hold_equity"] = (1 + df["stock_return"]).cumprod()

#5. Plot both equity curves together
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["strategy_equity"], label="MA Crossover Strategy", color='green')
plt.plot(df.index, df["buy_hold_equity"], label="Buy and Hold GOOG", color='blue', alpha=0.7)
plt.title("Strategy vs Buy and Hold: Growth of $1")
plt.xlabel("Date")
plt.ylabel("Equity (Starting at $1)")
plt.legend()
plt.grid(True)
plt.savefig("results/equity_curve.png")
plt.show()

#6. Save the full backtest results to a CSV for further analysis
df.to_csv("data/GOOG_backtest_results.csv")
print("\nBacktest results saved to data/GOOG_backtest_results.csv")

# Quick summary
final_strategy = df["strategy_equity"].iloc[-1]
final_buyhold = df["buy_hold_equity"].iloc[-1]
print(f"\nFinal Strategy Equity: ${final_strategy:.3f} (started at 1.0)")
print(f"Final Buy and Hold Equity: ${final_buyhold:.3f} (started at 1.0)")