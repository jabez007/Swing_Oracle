from datetime import datetime
import matplotlib.dates as mdates


class IntervalData(object):
    """
    Gives the data for a single time interval such as day, hour, or week
    """

    def __init__(self):
        """
        the ticker symbol that this interval belongs to
        """
        self.ticker = ""

        """
        the datetime that this interval represents
        :type datetimeStamp = datetime
        """
        self.datetimeStamp = datetime.now()

        """
        the price at the start of this interval
        :type open: float
        """
        self.open = 0.00

        """
        the highest price reached in this interval
        :type high: float
        """
        self.high = 0.00

        """
        the lowest price reached in this interval
        :type low: float
        """
        self.low = 0.00

        """
        the price at the end of this interval
        :type close: float
        """
        self.close = 0.00

        """
        the number of shares traded in this interval
        :type volume: int
        """
        self.volume = 0

        """
        the Relative Strength Index for this interval
        :type rsi: float
        """
        self.rsi = 0.00

    def to_vector(self):
        """
        gives a normalized vector representation of this interval
        :return: [open, high, low, close, volume]
        """
        return [self.open / 25.00,
                self.high / 25.00,
                self.low / 25.00,
                self.close / 25.00,
                self.volume / 1000000000.0]
                # self.rsi / 100]

    def to_plot(self):
        """
        gives the ohlc for this interval to be plotted on a candlestick chart
        :return: [date, open, high, low, close]
        """
        return [mdates.date2num(self.datetimeStamp),
                self.open,
                self.high,
                self.low,
                self.close]

    @staticmethod
    def from_json(symbol, datetime_stamp, json_data):
        """
        initializes an interval from the given json data
        :param symbol: the ticker symbol this interval data belongs to
        :param datetime_stamp: the datetime that starts this interval
        :param json_data: {
            "1. open": "",
            "2. high": "",
            "3. low": "",
            "4. close": "",
            "5. volume": "",
            "RSI": ""
        }
        :return: an initialized instance of IntervalData
        """
        interval_data = IntervalData()
        interval_data.ticker = symbol
        interval_data.datetimeStamp = datetime.strptime(datetime_stamp, "%Y-%m-%d")
        interval_data.open = float(json_data["1. open"])
        interval_data.high = float(json_data["2. high"])
        interval_data.low = float(json_data["3. low"])
        interval_data.close = float(json_data["4. close"])
        interval_data.volume = int(json_data["5. volume"])
        interval_data.rsi = float(json_data["RSI"])
        return interval_data

    @staticmethod
    def from_forecast(symbol, datetime_stamp, forecast_data):
        """

        :param symbol:
        :param datetime_stamp:
        :param forecast_data:
        :return:
        """
        interval_data = IntervalData()
        interval_data.ticker = symbol
        interval_data.datetimeStamp = datetime_stamp
        interval_data.open = forecast_data[0] * 25.00
        interval_data.high = forecast_data[1] * 25.00
        interval_data.low = forecast_data[2] * 25.00
        interval_data.close = forecast_data[3] * 25.00
        interval_data.volume = forecast_data[4] * 1000000000.0
        interval_data.rsi = forecast_data[5] * 100
        return interval_data
