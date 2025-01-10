import numpy as np

# yahoo finance library - historical and real time stock market data
import yfinance as yf

# date and time
from datetime import date, timedelta

# homemade modules
import operations

print("example ticker list = [AAPL, VOO, TSLA, GOOG, TXN, ...]")
ticker = input("give ticker of choice: ")
custom = input("custom timeline? y or n: ")
if custom == "y":
    start_date = input("give the start date, YYYY-MM-DD: ")
    end_date = input("give the end date, YYYY-MM-DD: ")
else: # default method, 1 YEAR from today
    end_date = date.today()
    start_date = date.today() - timedelta(days=365)

# fetching yf stock data
stockdata_yf = yf.download(ticker, start=start_date, end=end_date)
# storing data as a np.array
sdyf = np.array(stockdata_yf)

# moving average period in days
ma_days = int(input("give number of days (< " +str(len(sdyf)) +") for moving average calculations: "))

# printing a sample of yahoo finance data
print(ticker + " data from yahoo finance")
print("--------------------------------")
print(stockdata_yf)
print("--------------------------------")

print("Charting" + ticker + " between dates " + str(start_date) + ", " + str(end_date))

# performing calculations of SMA,EMA and generating and saving plots
operations.plot_stock_chart_yf(ticker, start_date, end_date, sdyf, len(sdyf), ma_days)
