from .IntervalData import IntervalData
from business_calendar import Calendar, PREVIOUS
from datetime import datetime
import matplotlib.dates as mdates

_holidays_ = [  # https://www.nyse.com/markets/hours-calendars
    "2018-01-01",  # New Years
    "2018-01-15",  # MLK day
    "2018-02-19",  # Washington's birthday
    "2018-03-30",  # Good Friday
    "2018-05-28",  # Memorial day
    "2018-07-04",  # Independence day
    "2018-09-03",  # Labor day
    "2018-11-22",  # Thanksgiving day
    "2018-12-25",  # Christmas
    ####
    "2019-01-01",  # New Years
    "2019-01-21",  # MLK day
    "2019-02-18",  # Washington's birthday
    "2019-04-19",  # Good Friday
    "2019-05-27",  # Memorial day
    "2019-07-04",  # Independence day
    "2019-09-02",  # Labor day
    "2019-11-28",  # Thanksgiving day
    "2019-12-25",  # Christmas
    ####
    "2020-01-01",  # New Years
    "2020-01-20",  # MLK day
    "2020-02-17",  # Washington's birthday
    "2020-04-10",  # Good Friday
    "2020-05-25",  # Memorial day
    "2020-07-03",  # Independence day
    "2020-09-07",  # Labor day
    "2020-11-26",  # Thanksgiving day
    "2020-12-25",  # Christmas
]
_calendar_ = Calendar(holidays=_holidays_)


class TimeSeries(object):
    """
    a collection of IntervalData objects for a specific ticker symbol
    """

    def __init__(self):
        """
        the ticker symbol this time series belongs to
        """
        self.ticker = ""

        """
        a list of datetime included in this time series (sorted oldest to newest)
        """
        self._datetimeStamps_ = list()

        """
        a dictionary of IntervalData representing this time series, with the key being the datetime of the IntervalData
        """
        self._intervals_ = dict()

    def get_input_output(self, x_size, y_size):
        """
        gathers the data from this time series into collections of vectors X and Y
        :param x_size:
        :param y_size:
        :return:
        """
        x = [[self._intervals_[d].to_vector() for d in self._datetimeStamps_[i: i + x_size]]
             for i in range(len(self._datetimeStamps_) - (x_size + y_size))]
        y = [[self._intervals_[d].to_vector() for d in self._datetimeStamps_[i + x_size: i + x_size + y_size]]
             for i in range(len(self._datetimeStamps_) - (x_size + y_size))]
        return x, y

    def get_seed(self, x_size):
        start_date = _calendar_.addbusdays(datetime.now(), -x_size).strftime("%Y-%m-%d")
        if start_date in self._datetimeStamps_:
            start_index = self._datetimeStamps_.index(start_date)
            return [self._intervals_[d].to_vector() for d in self._datetimeStamps_[start_index: start_index + x_size]]

    def get_plot(self):
        return [self._intervals_[d].to_plot() for d in self._datetimeStamps_]

    def get_volumes(self):
        return [mdates.date2num(self._intervals_[d].datetimeStamp) for d in self._datetimeStamps_], \
               [self._intervals_[d].volume for d in self._datetimeStamps_]

    def get_title(self):
        return "{ticker}({gain:.2f}%): {start} to {end}".format(ticker=self.ticker,
                                                                gain=self.get_max_gain() * 100,
                                                                start=self._datetimeStamps_[0],
                                                                end=self._datetimeStamps_[-1])

    def get_open(self):
        return self._intervals_[self._datetimeStamps_[0]].open

    def get_high(self):
        return (max(self._intervals_.values(), key=lambda x: x.high)).high

    def get_low(self):
        return (min(self._intervals_.values(), key=lambda x: x.low)).low

    def get_close(self):
        return self._intervals_[self._datetimeStamps_[-1]].close

    def get_max_gain(self):
        """
        find the Interval where the highest price is reached,
        then find the Interval before that where the lowest price is reached.
        From there, calculate the percent return.
        :return:
        """
        high_datapoint = max(self._intervals_.values(), key=lambda x: x.high)
        high_datetime = high_datapoint.datetimeStamp.strftime("%Y-%m-%d")
        high_index = self._datetimeStamps_.index(high_datetime)
        datetimes_subset = self._datetimeStamps_[:high_index + 1]  # include the interval with the high
        low_datapoint = min([self._intervals_[d] for d in datetimes_subset], key=lambda x: x.low)
        return (high_datapoint.high - low_datapoint.low) / low_datapoint.low

    @staticmethod
    def from_json(symbol, json_data):
        """
        initializes a time series from the given json data
        :param symbol: the ticker symbol this time series belongs to
        :param json_data: {
            "2018-06-18": {
            },
            "2018-06-19": {
            }
        }
        :return:
        """
        time_series = TimeSeries()
        time_series.ticker = symbol
        for date_time, data in json_data.items():
            time_series._datetimeStamps_ += [date_time]
            time_series._intervals_[date_time] = IntervalData.from_json(symbol, date_time, data)
        time_series._datetimeStamps_ = sorted(time_series._datetimeStamps_)
        return time_series

    @staticmethod
    def from_forecast(symbol, forecast):
        """

        :param symbol:
        :param forecast:
        :return:
        """
        time_series = TimeSeries()
        time_series.ticker = symbol
        '''
        since the construction of DAILY ignores data from today's date (so as not to use incomplete data)
        the forecast will technically start on today's date or the latest business date
        '''
        date_time = _calendar_.adjust(datetime.now(), PREVIOUS)
        for data in forecast:
            time_series._datetimeStamps_ += [date_time.strftime("%Y-%m-%d")]
            time_series._intervals_[date_time.strftime("%Y-%m-%d")] = IntervalData.from_forecast(symbol,
                                                                                                 date_time, data)
            date_time = _calendar_.addbusdays(date_time, 1)
        time_series._datetimeStamps_ = sorted(time_series._datetimeStamps_)
        return time_series
