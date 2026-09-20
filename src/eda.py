import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned data
df = pd.read_csv("data/GOOG_clean.csv", index_col=0, parse_dates=True)

#1. Plot the closing price over time
plt.figure(figsize=(12, 5))
plt.plot(df.index, df["Close"], label="GOOG Close Price", color='blue')
plt.title("GOOG Closing Price (2015-2025)")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.savefig("results/goog_price_chart.png")
plt.show()

#2 Calculate daily returns
df["daily_return"] = df["Close"].pct_change()

#3 Basic statistics on daily returns
print("\nBasic statistics on daily returns:")
print(df["daily_return"].describe())

#4. Plot histogram of daily returns
plt.figure(figsize=(8, 5))
df["daily_return"].hist(bins=50, color='purple')
plt.title("Histogram of GOOG Daily Returns")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.savefig("results/goog_returns_distribution.png")
plt.show()