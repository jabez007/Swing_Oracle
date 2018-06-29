from data import DAILY
import oracle
from pprint import pprint
from screener import TICKERS
import sys

if len(sys.argv) == 2:
    sys_argv = str.upper(sys.argv[1])

    if sys_argv == "TRAIN":
        print("-- Train option selected")
        oracle.train()
    elif sys_argv == "FORECAST":
        print("-- Forecast option selected")
        for t in TICKERS:
            print("Running forecast for " + t["ticker"])
            forecast = oracle.get_forecast(t["ticker"])
            if forecast is not None:
                if ((forecast.get_high() - forecast.get_open()) / forecast.get_open()) >= 0.1:
                    print("\twinner:", forecast.get_open(), forecast.get_high())
                if ((forecast.get_low() - forecast.get_open()) / forecast.get_open()) <= -0.1:
                    print("\tloser:", forecast.get_open(), forecast.get_low())
            # input("Press Enter to continue...")
    else:
        print("-- Getting latest for " + sys_argv)
        x = DAILY[sys_argv].get_seed(20)
        pprint(x)
else:
    print("-- No option given")
    print(DAILY["PLUG"].get_open())
    print(DAILY["PLUG"].get_high())
    print(DAILY["PLUG"].get_low())
    print(DAILY["PLUG"].get_close())
