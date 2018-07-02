# https://pythonprogramming.net/candlestick-ohlc-graph-matplotlib-tutorial/
from matplotlib import style
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc

style.use('ggplot')


def from_timeseries(forecast):
    ohlc = forecast.get_plot()
    # date, open, high, low, close
    
    fig = plt.figure()
    
    # prices
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    
    # use green for rises and red for falls
    candlestick_ohlc(ax1, ohlc, width=0.9, colorup='#77d879', colordown='#db3f3f')
    
    # converts the axis from the raw mdate numbers to dates.
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(forecast.get_title())
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    # plt.show()
    fig.savefig("figure.png", bbox_inches='tight')
    plt.close(fig)
    return "figure.png"
