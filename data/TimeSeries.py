from .IntervalData import IntervalData


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
