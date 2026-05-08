import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create folders
os.makedirs("outputs", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("data", exist_ok=True)

# -----------------------------------
# STOCK CONFIGURATION
# -----------------------------------

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2025-01-01"

# -----------------------------------
# FETCH STOCK DATA
# -----------------------------------

print("Fetching stock data...")

df = yf.download(ticker, start=start_date, end=end_date)

# Fix MultiIndex columns issue
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

print("Data fetched successfully!")

# Save CSV backup
df.to_csv(f"data/{ticker}_stock_data.csv")

# -----------------------------------
# DATA CLEANING
# -----------------------------------

df.dropna(inplace=True)

# -----------------------------------
# DAILY RETURNS
# -----------------------------------

df["Daily Return"] = df["Close"].pct_change()

# -----------------------------------
# MOVING AVERAGES
# -----------------------------------

df["SMA20"] = df["Close"].rolling(window=20).mean()
df["SMA50"] = df["Close"].rolling(window=50).mean()

# -----------------------------------
# VOLATILITY
# -----------------------------------

volatility = df["Daily Return"].std()

# -----------------------------------
# PRICE ANALYSIS
# -----------------------------------

highest_price = df["High"].max()
lowest_price = df["Low"].min()

latest_close = df["Close"].iloc[-1]

average_return = df["Daily Return"].mean()

# -----------------------------------
# REPORT GENERATION
# -----------------------------------

report = f"""
STOCK MARKET ANALYSIS REPORT
=============================

Ticker: {ticker}

Highest Price: {highest_price:.2f}
Lowest Price: {lowest_price:.2f}

Average Daily Return:
{average_return:.5f}

Volatility:
{volatility:.5f}

Latest Closing Price:
{latest_close:.2f}
"""

print(report)

# Save report
with open(f"reports/{ticker}_report.txt", "w") as file:
    file.write(report)

# -----------------------------------
# CLOSING PRICE CHART
# -----------------------------------

plt.figure(figsize=(12,6))

plt.plot(df.index, df["Close"], label="Closing Price")

plt.title(f"{ticker} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.savefig(f"outputs/{ticker}_closing_price.png")

plt.close()

# -----------------------------------
# MOVING AVERAGE CHART
# -----------------------------------

plt.figure(figsize=(12,6))

plt.plot(df.index, df["Close"], label="Close")
plt.plot(df.index, df["SMA20"], label="SMA20")
plt.plot(df.index, df["SMA50"], label="SMA50")

plt.title(f"{ticker} Moving Average Analysis")

plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.savefig(f"outputs/{ticker}_moving_average.png")

plt.close()

# -----------------------------------
# DAILY RETURNS HISTOGRAM
# -----------------------------------

plt.figure(figsize=(10,5))

df["Daily Return"].hist(bins=50)

plt.title("Daily Return Distribution")
plt.xlabel("Return")
plt.ylabel("Frequency")

plt.savefig(f"outputs/{ticker}_daily_returns.png")

plt.close()

print("Charts generated successfully!")
print("Project completed successfully!")