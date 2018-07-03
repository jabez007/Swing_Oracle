import configuration_manager
from data import DAILY
import oracle
from pprint import pprint
from screener import TICKERS
import sys
import twitter


def train():
    print("-- Train option selected")
    oracle.train()


def forecast():
    print("-- Forecast option selected")
    tweet = twitter.Api(consumer_key=configuration_manager.AppSettings["twitter"]["consumer key"],
                        consumer_secret=configuration_manager.AppSettings["twitter"]["consumer secret"],
                        access_token_key=configuration_manager.AppSettings["twitter"]["access token key"],
                        access_token_secret=configuration_manager.AppSettings["twitter"]["access token secret"])

    for t in TICKERS:
        print("Running forecast for " + t["ticker"])
        _forecast = oracle.get_forecast(t["ticker"])
        if _forecast is not None:
            if _forecast.get_max_gain() >= 0.1:
                figure = oracle.Plot.from_timeseries(_forecast)
                # input("Press Enter to continue...")
                tweet.PostUpdate(status=_forecast.get_title(),
                                 media=figure)


if len(sys.argv) == 2:
    sys_argv = str.upper(sys.argv[1])
    if sys_argv == "TRAIN":
        train()
    elif sys_argv == "FORECAST":
        forecast()
    else:
        print("-- invalid option selected")
else:
    train()
    forecast()
