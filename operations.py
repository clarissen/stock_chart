import numpy as np
import matplotlib.pyplot as plt
import os


# ----------------------
# FUNCTIONS
# ----------------------
# ==================================================================================

# plotting stock performance from yf
# makes 4 plots: 
# - opening and closing prices per day
# - high and low prices per day
# - trading volume per day
# - comprehensive plot with closing, volumes, and SMA + EMA
def plot_stock_chart_yf(ticker, start, end, data, days, ma_days):

    linestylesdash = ['k-.', 'r-.', 'b--', 'g:', 'm-.', 'y:']
    linestyles = ["k", "r", "b", "g", "m-.", "y-."]

    opens = data[:,3]
    closes = data[:,0]

    highs = data[:,1]
    lows = data[:,2]

    volumes = data[:,4] / 1e6

    trading_days = np.arange(0,days)

    fig,ax = plt.subplots()

    ax.plot(trading_days, opens, linestyles[0], label = "opening price (USD)")
    ax.plot(trading_days, closes, linestyles[2], label ="closing price (USD) ")
    ax.set_xlabel("trading days ("+ str(start) + ", " + str(end) +")" )
    ax.set_ylabel("Value (USD)")
    ax.set_title("Daily opening and closing prices for " + ticker)
    ax.legend()
    # ax.legend(loc = "upper right")
    save_loc = "./plots/"
    if not os.path.exists(save_loc):
        os.makedirs(save_loc)
    plt.savefig(save_loc + ticker +"_open_close.png")

    ax.clear()
    ax.plot(trading_days, highs, linestyles[3], label = "Highest price (USD)")
    ax.plot(trading_days, lows, linestyles[1], label ="Lowest price (USD) ")
    ax.set_xlabel("trading days ("+ str(start) + ", " + str(end) +")" )
    ax.set_ylabel("Value (USD)")
    ax.set_title("Daily high and low prices for " + ticker)
    ax.legend()
    plt.savefig(save_loc + ticker +"_high_low.png")

    ax.clear()
    ax.plot(trading_days, volumes, linestyles[4], label = "Number of trades")
    ax.set_xlabel("trading days ("+ str(start) + ", " + str(end) +")" )
    ax.set_ylabel("Number of trades (millions)")
    ax.set_title("Daily trading volume for " + ticker)
    ax.legend()
    plt.savefig(save_loc + ticker +"_volume.png")

    # comprehensive stock chart with volumes, closing price, SMA, EMA
    sma, ema = moving_averages(closes, ma_days)

    ax.clear()
    ax.plot(trading_days, closes, linestyles[2], label ="closing price (USD) ")
    ax.plot(trading_days[ma_days:], sma, linestyles[5], label ="SMA")
    ax.plot(trading_days[ma_days:], ema, linestyles[4], label ="EMA")
    ax.set_ylabel("Value (USD)")

    ax2 = ax.twinx()
    ax2.bar(trading_days, volumes, alpha = 0.25, color = "k", label = "Volume")
    ax2.set_ylabel("Number of trades (millions)")

    ax.set_xlabel("trading days ("+ str(start) + ", " + str(end) +")" )
    ax.set_title("Stock chart with " +str(ma_days) + " day moving averages for " + ticker)
    ax.legend()
    ax2.legend(loc="lower right")
    plt.savefig(save_loc + ticker +"_comprehensive.png")


    print("plots saved in " + save_loc)

def moving_averages(closes, ma_days):

    #simple moving average
    sma = []
    for i in range(0,len(closes)):
        sma_i = sum(closes[i:ma_days+i])/ma_days
        sma.append(sma_i)

    # we only want the first N=ma_days elements 
    # e.g. because we cannot calculate the N day average during the first N days
    sma_out = np.array(sma[:-ma_days])


    #exponential moving average
    smoothing = 2/(ma_days+1)
    # the first ema data point is the SMA of the first N days closing prices
    # or the first SMA data point
    ema = [sma_out[0]]
    for i in range(1,len(closes)-ma_days):
        ema_i = smoothing*closes[ma_days+i] + (1- smoothing)*ema[i-1]
        ema.append(ema_i)

    ema_out = np.array(ema)
    # the EMA seems to be a more sensitive prediction tool during 
    # regions of higher market volatility

    return sma_out, ema_out










# ==================================================================================
