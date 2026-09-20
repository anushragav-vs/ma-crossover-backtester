import pandas as pd

# Load the raw csv
# Header=[0.1] handles yfinance's multi-level column format
# Index_col=0 tells pandas to use the first column as the index
df = pd.read_csv("data/GOOG_daily.csv", header=0, index_col=0)
df.index = pd.to_datetime(df.index, format="%Y-%m-%d", errors='coerce')  #convert index to datetime
df.index.name = "Date"  #rename index to "Date"

# yfinance sometimes adds an extra header row-drop it if it exists
df = df[pd.to_numeric(df["Close"], errors='coerce').notnull()]

# Convert all price/volume columns to proper numeric types
for col in ["Open", "High", "Low", "Close", "Volume"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    
# Check for missing values
print("Missing values in each column:")
print(df.isnull().sum())

# Drop rows with missing values
df = df.dropna()

# Sort by date just in case
df = df.sort_index()

print(f"\nCleaned dataset shape: {df.shape}")
print(df.head())  # Display the first few rows of the cleaned data
print(df.tail())  # Display the last few rows of the cleaned data

# Save the cleaned data to a new CSV file
df.to_csv("data/GOOG_clean.csv")
print("\nCleaned data saved to data/GOOG_clean.csv")
