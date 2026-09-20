import yfinance as yf
import pandas as pd

# Download daily historical data for GOOG
ticker = 'GOOG'
data = yf.download(ticker, start='2015-01-01', end='2025-01-01')

# Check that we actually got data
if data.empty:
    print("No data downloaded.Check your internet connection or the ticker symbol.")
else:
    print(f"Downloaded {len(data)} rows of data for {ticker}.")
    print(data.head())  # Display the first few rows of the data
    
    # Save the data to a CSV file
    data.to_csv("data/GOOG_daily.csv")
    print("Data saved to data/GOOG_daily.csv")