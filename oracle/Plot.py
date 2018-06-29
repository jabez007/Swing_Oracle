# https://pythonprogramming.net/candlestick-ohlc-graph-matplotlib-tutorial/
# https://pythonprogramming.net/more-stock-data-manipulation-python-programming-for-finance/
from matplotlib import style
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

style.use('ggplot')


def from_timeseries(forecast):
    ohlc = forecast.get_plot()
    # date, open, high, low, close
    volume_dates, volume_values = forecast.get_volumes()
    
    fig = plt.figure()
    
    # prices
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    # volume
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    
    # use green for rises and red for falls
    candlestick_ohlc(ax1, ohlc, width=5, colorup='g')
    ax2.fill_between(volume_dates, volume_values, 0)

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    
    # converts the axis from the raw mdate numbers to dates.
    # ax1.xaxis_date()
    
    # format datetime data on the x axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
    # set the number of x labels we want
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    
    # ax1.grid(True)
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock)
    # plt.legend()
    # plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()
