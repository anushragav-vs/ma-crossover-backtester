import pandas as pd

def load_csv(filepath):
    """Load a CSV with a datetime index - used across all scripts."""
    return pd.read_csv(filepath, index_col=0, parse_dates=True)