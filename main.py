from data import DAILY
import oracle
from pprint import pprint
from screener import TICKERS
import sys

if len(sys.argv) == 2:
    sys_argv = str.upper(sys.argv[1])

    if sys_argv == "TRAIN":
        print("Train option selected")
        oracle.train()
    elif sys_argv == "FORECAST":
        print("Forecast option selected")
        for t in TICKERS:
            oracle.forecast(t["ticker"])
    else:
        print("Getting latest for " + sys_argv)
        x = DAILY[sys_argv].get_seed(20)
        pprint(x)
else:
    print("No option given")
    x = DAILY["PLUG"].get_seed(20)
    pprint(x)
    print(len(x))
