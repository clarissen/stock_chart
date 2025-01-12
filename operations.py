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
def plot_stock_chart_yf(ticker, start, end, data, days, ma_days, so_days):

    plt.rcParams['figure.figsize'] = [12, 4]

    linestylesdash = ['k-.', 'r-.', 'b--', 'g:', 'm-.', 'y:']
    linestyles = ["k", "r", "b", "g", "m", "y"]

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

    # stochastic oscillator 
    so, so_sma3 = stochastic_oscillator(closes, highs, lows, so_days)

    ax.clear()
    ax.plot(trading_days[so_days:], so, linestyles[1], label="%K, " + str(so_days)+" days")
    ax.plot(trading_days[so_days+3:], so_sma3, linestyles[2], label="%D, 3 day SMA of %K")
    ax.plot(trading_days, 80*np.ones(len(trading_days)), linestylesdash[0] )
    ax.plot(trading_days, 20*np.ones(len(trading_days)), linestylesdash[0] )
    ax.set_ylabel("Stochastic Value (%)")

    ax.set_xlabel("trading days ("+ str(start) + ", " + str(end) +")" )
    ax.set_title(" Fast stochastic oscillator (%K) with a 3 day SMA (%D) for " + ticker)
    ax.legend()
    plt.savefig(save_loc + ticker +"_stochastics.png")

    # macd and signal lines
    macd, macd_shift, sig, sig_shift = ma_converg_diverg(closes)

    ax.clear()
    ax.plot(trading_days[macd_shift:], macd, linestyles[1], label="MACD")
    ax.plot(trading_days[sig_shift:], sig, linestyles[2], label="Signal")

    ax.set_ylabel("Value (USD)")

    ax.set_xlabel("trading days ("+ str(start) + ", " + str(end) +")" )
    ax.set_title("MACD and signal line for " + ticker)
    ax.legend()
    plt.savefig(save_loc + ticker +"_macd_sig.png")



    # comprehensive stock chart with volumes, closing price, SMA, EMA
    sma = simple_ma(closes, ma_days)
    ema = exp_ma(closes, ma_days, sma)

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


def simple_ma(closes, ma_days):

    #simple moving average
    sma = []
    for i in range(0,len(closes)-ma_days):
        sma_i = sum(closes[i:ma_days+i])/ma_days
        sma.append(sma_i)

    # we only want the first N=ma_days elements 
    # i.e. we cannot calculate the N day average during the first N days
    sma_out = np.array(sma)

    return sma_out

def exp_ma(closes, ma_days, sma):
    #exponential moving average
    smoothing = 2/(ma_days+1)
    # the first ema data point is the SMA of the first N days closing prices
    # or the first SMA data point
    ema = [sma[0]]
    for i in range(1,len(closes)-ma_days):
        ema_i = smoothing*closes[ma_days+i] + (1- smoothing)*ema[i-1]
        ema.append(ema_i)

    ema_out = np.array(ema)
    # the EMA seems to be a more sensitive prediction tool during 
    # regions of higher market volatility

    return ema_out

def stochastic_oscillator(closes, highs, lows, so_days):

    # stochastic oscillator
    so = []
    

    for i in range(0,len(closes)-so_days):
        # most recent closing price
        C = closes[i+so_days-1]
        # lowest low price over the period
        L = min(lows[i:i+so_days])
        # highest high price over the period
        H = max(highs[i:i+so_days])

        # calculating each stochastic value as a percentage
        sv = (C - L )/(H - L) * 100
        so.append(sv)
        

    so = np.array(so)

    # 3 period simple moving average of the stochastic oscillator
    so_sma3 = []

    for i in range(0,len(so)-3):
        sv_sma3 = sum(so[i:3+i]) / 3
        so_sma3.append(sv_sma3)

    return so, np.array(so_sma3)


def ma_converg_diverg(closes):

    # calculating the sma as inputs for ema

    sma_26 = simple_ma(closes, 26)

    sma_12 = simple_ma(closes, 12)

    ema_26 = exp_ma(closes, 26, sma_26)

    ema_12 = exp_ma(closes, 12, sma_12)

    # we must select only the shared period of data
    macd = ema_12[(26-12):] - ema_26

    sig = exp_ma(macd, 9, macd)

    # returning the macd and signal and the length of time data we do not have for them
    return macd, len(closes)-len(macd), sig, len(closes) - len(sig)



# Extra notes:


        # checks ran in the stochastic oscillator during index debugging
        # ----------------------
        # if C <= L:
        #     print("C <= L at i = ", i)
        #     print("-----------------")
        #     print("closing = ", closes[i+so_days])
        #     print("lows =", lows[i:i+so_days])
        # if H <= L:
        #     print("H <= L at i = ", i)
        #     print("-----------------")
        #     print("highs =", highs[i:i+so_days])
        #     print("lows =", lows[i:i+so_days])

        # print("C-L = ", C-L)
        # print("H-L", H-L)
        # ----------------------







# ==================================================================================
