import pandas as pd
import numpy as np


def load_signals(path):
    return pd.read_csv(path, index_col=0, parse_dates=True)


def calc_metrics(returns, position):
    equity = (1 + returns).cumprod()
    years = len(returns) / 252
    return {
        "CAGR": equity.iloc[-1] ** (1 / years) - 1,
        "Sharpe": returns.mean() / returns.std() * np.sqrt(252),
        "MaxDrawdown": (equity / equity.cummax() - 1).min(),
        "Trades": int(position.diff().abs().sum()),
    }


v1 = load_signals("data/GOOG_with_signals.csv")
v2 = load_signals("data/GOOG_with_signals_v2.csv")
stock_ret = v2["Close"].pct_change()

# Same evaluation window as before: start when the 200-day MA exists
start = v2["MA_200"].first_valid_index()
idx = v2.loc[start:].index


def net_returns(position, cost):
    """Daily strategy return after subtracting trading costs."""
    pos = position.loc[idx]
    gross = pos * stock_ret.loc[idx]
    trade_cost = pos.diff().abs().fillna(0) * cost   # cost only on days position changes
    return gross - trade_cost


rows = []
for cost_bps in [0, 5, 10, 20]:
    cost = cost_bps / 10000          # convert bps to a fraction
    for name, data in [("V1 (20/50)", v1), ("V2 (+200 filter)", v2)]:
        net = net_returns(data["position"], cost)
        m = calc_metrics(net, data["position"].loc[idx])
        rows.append({"Strategy": name, "Cost_bps": cost_bps, **m})

table = pd.DataFrame(rows)
table.to_csv("results/cost_analysis.csv", index=False)

# Buy & hold reference (a single trade, so cost is negligible)
bh = stock_ret.loc[idx]
bh_m = calc_metrics(bh, pd.Series(1.0, index=idx))
print(f"Buy & Hold reference: CAGR {bh_m['CAGR']:.2%}, Sharpe {bh_m['Sharpe']:.2f}, "
      f"MaxDD {bh_m['MaxDrawdown']:.2%}\n")

# Readable printout
show = table.copy()
show["CAGR"] = (show["CAGR"] * 100).round(2).astype(str) + "%"
show["MaxDrawdown"] = (show["MaxDrawdown"] * 100).round(2).astype(str) + "%"
show["Sharpe"] = show["Sharpe"].round(2)
print(show.to_string(index=False))