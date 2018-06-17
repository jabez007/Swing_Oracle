import collections
import configuration_manager
import json
import os
import requests

_api_key_ = configuration_manager.AppSettings["alpha vantage"]
_data_path_ = os.path.dirname(os.path.realpath(__file__))
_daily_json_ = os.path.join(_data_path_, 'daily.json')


def _download_daily_full_(symbol):
    data = dict()
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+symbol+"&outputsize=full&apikey="+_api_key_)
    _data = r.json()
    data["Symbol"] = _data["Meta Data"]["2. Symbol"]
    data["Daily"] = collections.OrderedDict(sorted(_data["Time Series (Daily)"].items()))
    return data
