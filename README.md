# stock_chart
python script that generates a daily stock chart with moving averages from yahoo finance data accessed from yfinance library. There are example stock charts made for VOO for the period (2024-01-10, 2025-01-09)

# packages
make sure you have the yahoo finance library up to date:

pip install yfinance

# to run code
python<version> main.py

# what you can input to the code
give ticker of choice: ____
custom timeline? y or n: ____
give the start date, YYYY-MM-DD: _________
give the end date, YYYY-MM-DD: _________
give number of days for moving average calculations: ___
give number of days for stochastic oscillator: ____

# what the code visualizes
in the custom module operations.py, 4 plots are made
1. a plot of opening and closing prices for each day
2. a plot of high and low prices for each day
3. a plot of daily trading volumes as a line plot
4. a comprehensive plot of closing prices (Left y-axis) for each day and daily trading volumes as a bar graph (Right y-axis). From the closing prices the simple moving average (SMA) and exponential moving average (EMA) are calculated with number of days for the averaging calculation given as an input from the terminal.
5. a fast stochastic oscillator (%K) plot with a 3 day SMA of the stochastic oscillator (%D)
All of these plots will be saved as .png files with respective names in a folder called ./plots/

# what the code calculates
in operations.py, we explicitly calculate, using nothing but the numpy library, the following:

Simple moving average: 
----------------------
sma = sum of the closing prices for N days / ( N )

Exponential moving average:
----------------------
Given the first data point of the simple moving average as input, ema_n-1, the exponential moving average on day n, ema_n, is calculated from closing prices on day n, CP_n, using a smoothing factor a = 2 / (n + 1):

ema_n = a * CP_n + (1- a)*ema_n-1

Stochastic Oscillator:
----------------------
Calculating a fast stochastic oscillator over a period of n days, with values %K using most recent closing price C_n-1, highest high price H, lowest low price L
%K = 100*(C-L)/(H-L)

Also using a SMA of 3 day period on the %K data
%D = sum(%K over 3 days) / 3 days

Moving Average Convergence/Divergence (MACD)
----------------------
The MACD:
compute the exponential moving average:
ema_n = a * CP_n + (1- a)*ema_n-1
for the 12 day period and subtract from it the 26 day period EMA.
The signal line, used to study where the MACD and signal lines crossover, is computed from the 9 day EMA of the MACD.
In principle, choices of period can be modified but 26,12,9 are standard.