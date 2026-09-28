import pandas as pd


def add_moving_averages(df, fast_window=20, slow_window=50, trend_window=200):
    """Add fast, slow, and long-term trend moving averages."""
    df[f"MA_{fast_window}"] = df["Close"].rolling(window=fast_window).mean()
    df[f"MA_{slow_window}"] = df["Close"].rolling(window=slow_window).mean()
    df[f"MA_{trend_window}"] = df["Close"].rolling(window=trend_window).mean()
    return df


def generate_signals(df, fast_window=20, slow_window=50, trend_window=200, use_trend_filter=True):
    """
    Generate a trading signal column:
    1 = long position
    0 = flat (no position)
    If use_trend_filter is True, we only go long when price is above the trend MA.
    """
    fast_col = f"MA_{fast_window}"
    slow_col = f"MA_{slow_window}"
    trend_col = f"MA_{trend_window}"

    df["Signal"] = 0
    crossover_long = df[fast_col] > df[slow_col]

    if use_trend_filter:
        trend_up = df["Close"] > df[trend_col]
        df.loc[crossover_long & trend_up, "Signal"] = 1
    else:
        df.loc[crossover_long, "Signal"] = 1

    # Shift by 1 day: we can only act on a signal the day AFTER it appears
    # (avoids look-ahead bias)
    df["position"] = df["Signal"].shift(1)
    return df


if __name__ == "__main__":
    df = pd.read_csv("data/GOOG_clean.csv", index_col=0, parse_dates=True)
    df = add_moving_averages(df)
    df = generate_signals(df, use_trend_filter=True)

    print(df[["Close", "MA_20", "MA_50", "MA_200", "Signal", "position"]].tail(15))

    df.to_csv("data/GOOG_with_signals_v2.csv")
    print("\nSaved data/GOOG_with_signals_v2.csv")