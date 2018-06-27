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
        x, y = DAILY[sys_argv].get_input_output(20, 1)
        pprint(y[-1])
else:
    print("No option given")
