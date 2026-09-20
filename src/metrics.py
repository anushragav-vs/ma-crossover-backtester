import pandas as pd
import numpy as np

df = pd.read_csv("data/GOOG_backtest_results.csv", index_col=0, parse_dates=True)

def calculate_metrics(equity_series, return_series, label):
    # Number of years covered in the backtest
    n_days = len(equity_series)
    n_years = n_days / 252  # Approximate number of trading days in a year
    
    # CAGR (Compound Annual Growth Rate)
    total_growth = equity_series.iloc[-1] / equity_series.iloc[0]
    cagr = total_growth ** (1 / n_years) - 1
    
    # Annualized Volatility
    annual_vol = return_series.std() * np.sqrt(252)
    
    # Sharpe Ratio (assuming risk-free rate = 0)
    sharpe = (return_series.mean() / return_series.std()) * np.sqrt(252)
    
    # Maximum Drawdown
    running_max = equity_series.cummax()
    drawdown = (equity_series / running_max) - 1
    max_drawdown = drawdown.min()
    
    print(f"\n---{label}---")
    print(f"CAGR: {cagr:.2%}")
    print(f"Annualized Volatility: {annual_vol:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    
    return {"CAGR": cagr, "Volatility": annual_vol, "Sharpe": sharpe, "MaxDrawdown": max_drawdown}

strategy_metrics = calculate_metrics(df["strategy_equity"], df["strategy_return"], "MA CrossoverStrategy")
buyhold_metrics = calculate_metrics(df["buy_hold_equity"], df["stock_return"], "Buy and Hold GOOG")

# Save metrics to a CSV for further analysis
results_df = pd.DataFrame([strategy_metrics, buyhold_metrics], index=["Strategy", "Buy and Hold"])
results_df.to_csv("results/performance_metrics.csv")
print("\nPerformance metrics saved to results/performance_metrics.csv")