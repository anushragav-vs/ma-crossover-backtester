import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_signals(path):
    return pd.read_csv(path, index_col=0, parse_dates=True)


def calc_metrics(returns, position):
    """Performance metrics from a series of daily returns."""
    equity = (1 + returns).cumprod()
    years = len(returns) / 252
    cagr = equity.iloc[-1] ** (1 / years) - 1
    vol = returns.std() * np.sqrt(252)
    sharpe = returns.mean() / returns.std() * np.sqrt(252)
    max_dd = (equity / equity.cummax() - 1).min()
    trades = int(position.diff().abs().sum())   # each entry or exit = 1 trade
    time_in_market = position.mean()
    return {
        "CAGR": cagr,
        "Volatility": vol,
        "Sharpe": sharpe,
        "MaxDrawdown": max_dd,
        "Trades": trades,
        "TimeInMarket": time_in_market,
    }


# 1. Load both versions
v1 = load_signals("data/GOOG_with_signals.csv")
v2 = load_signals("data/GOOG_with_signals_v2.csv")

# 2. Daily returns: stock itself, and each strategy (position x stock return)
stock_ret = v2["Close"].pct_change()
results = pd.DataFrame({
    "stock": stock_ret,
    "v1": v1["position"] * v1["Close"].pct_change(),
    "v2": v2["position"] * stock_ret,
})

# 3. Same evaluation window for all: start when the 200-day MA first exists
start = v2["MA_200"].first_valid_index()
results = results.loc[start:].dropna()
print(f"Evaluation window: {results.index[0].date()} to {results.index[-1].date()}")

# 4. Metrics for each
ones = pd.Series(1.0, index=results.index)   # buy & hold = always in the market
table = pd.DataFrame({
    "Buy & Hold": calc_metrics(results["stock"], ones),
    "V1 (20/50)": calc_metrics(results["v1"], v1["position"].loc[results.index]),
    "V2 (+200 filter)": calc_metrics(results["v2"], v2["position"].loc[results.index]),
}).T

table.to_csv("results/version_comparison.csv")

# 5. Print in readable form
display = table.copy()
for col in ["CAGR", "Volatility", "MaxDrawdown", "TimeInMarket"]:
    display[col] = (display[col] * 100).round(2).astype(str) + "%"
display["Sharpe"] = display["Sharpe"].round(2)
display["Trades"] = display["Trades"].astype(int)
print()
print(display)

# 6. Equity curves
equity = (1 + results[["stock", "v1", "v2"]]).cumprod()
plt.figure(figsize=(12, 6))
plt.plot(equity.index, equity["stock"], label="Buy & Hold", color="blue", alpha=0.7)
plt.plot(equity.index, equity["v1"], label="V1: 20/50 crossover", color="darkgreen")
plt.plot(equity.index, equity["v2"], label="V2: + 200-day trend filter", color="orange")
plt.title("V1 vs V2 vs Buy & Hold: Growth of $1 (same window)")
plt.xlabel("Date")
plt.ylabel("Equity")
plt.legend()
plt.grid(True)
plt.savefig("images/v1_vs_v2_equity.png", dpi=150)
plt.show()