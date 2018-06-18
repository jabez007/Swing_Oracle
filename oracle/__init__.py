SEQUENCE_LEN = 20


def format_daily_data(raw_json):
    """
    formats the time series data for a ticker symbol into the X and Y for a LSTM model
    :param raw_json: {
                        "ABC": {
                            "2018-06-17": {
                            },
                            "2018-06-18": {
                            }
                        },
                        "DEF": {
                            "2018-06-17": {
                            },
                            "2018-06-18": {
                            }
                        }
                     }
    :return: x and y for the input and output of a LSTM model
    """
    x, y = list(), list()

    for symbol, dates in raw_json.items():
        _x = list()
        for date, data in dates.items():
            if len(_x) < SEQUENCE_LEN:
                _x += [[data["1. open"],
                       data["2. high"],
                       data["3. low"],
                       data["4. close"],
                       data["5. volume"]]]
            else:
                x += [_x]
                y += [[data["1. open"],
                      data["2. high"],
                      data["3. low"],
                      data["4. close"],
                      data["5. volume"]]]

                _x = [[data["1. open"],
                      data["2. high"],
                      data["3. low"],
                      data["4. close"],
                      data["5. volume"]]]

    return x, y
