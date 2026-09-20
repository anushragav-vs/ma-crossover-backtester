import pandas as pd

def add_moving_averages(df, fast_window=20, slow_window=50):
    """
    Adds fast and slow moving averages to the DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with a 'Close' column.
    fast_window (int): Window size for the fast moving average.
    slow_window (int): Window size for the slow moving average.
    
    Returns:
    pd.DataFrame: DataFrame with added moving average columns.
    """
    df[f"MA_{fast_window}"] = df["Close"].rolling(window=fast_window).mean()
    df[f"MA_{slow_window}"] = df["Close"].rolling(window=slow_window).mean()
    return df
def generate_signals(df, fast_window=20, slow_window=50):
    """
    Generate a trading signal column:
    1 = holding a long position
    0 = flat(no position)"""
    fast_col = f"MA_{fast_window}"
    slow_col = f"MA_{slow_window}"
    
    df["Signal"] = 0
    # Where fast SMA > slow SMA, set signal to 1 (long position)
    df.loc[df[fast_col] > df[slow_col], "Signal"] = 1
    
    # Shift signal by 1 day: we can only act on a crossover
    # The day after it happens(avoids look-ahead bias)
    df["position"] = df["Signal"].shift(1)
    return df

if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("data/GOOG_clean.csv", index_col=0, parse_dates=True)
    df = add_moving_averages(df)
    df = generate_signals(df)
    
    print(df[["Close","MA_20","MA_50","Signal","position"]].tail(15))  # Display the last 15 rows of relevant columns
    
    df.to_csv("data/GOOG_with_signals.csv")
    print("\nData with moving averages and signals saved to data/GOOG_with_signals.csv")