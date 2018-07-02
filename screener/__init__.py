import configuration_manager
import json
import os
import requests

_screener_path_ = os.path.dirname(os.path.realpath(__file__))
_screener_json_ = os.path.join(_screener_path_, 'screener.json')


def _load_(tickers=list()):
    """
    loads the locally cached ticker symbols found from our search parameters
    :param tickers: any already loaded or downloaded ticker symbols
    :return: the list of locally cached ticker symbols
    """
    print("-- Loading ticker symbols that meet our search criteria")
    for f in os.listdir(_screener_path_):
        if f.endswith(".json"):
            with open(os.path.join(_screener_path_, f)) as f_json:
                data = json.load(f_json)
            if "data" not in data:
                tickers += data
            else:
                for d in data["data"]:
                    if not any(d["ticker"] == t["ticker"] for t in tickers):
                        tickers += [d]
    # tickers = _download_(tickers)
    _save_(tickers)
    return tickers


def _download_(tickers, page=1):
    """
    downloads a list of ticker symbols that have a 52 Week Low >= $1.00 and a 52 Week High <= $25.00, with a Market
    Capitalization between $300,000,000 and $2,000,000,000, and an Average Daily Volume over 500,000
    :param tickers:
    :param page:
    :return: the list of ticker symbols downloaded from the screener that meet our search parameters
    """
    r = requests.get("https://api.intrinio.com/securities/search?conditions=52_week_low~gte~1.00,52_week_high~lte~25.00,marketcap~gte~300000000,marketcap~lte~2000000000,average_daily_volume~gte~500000&page_number=" + str(page),
                     auth=(configuration_manager.AppSettings["intrinio"]["api username"],
                           configuration_manager.AppSettings["intrinio"]["api password"]))

    data = r.json()
    for d in data["data"]:
        if not any(d["ticker"] == t["ticker"] for t in tickers):
            tickers += [d]

    if page < data["total_pages"]:
        return _download_(tickers, page+1)
    else:
        return tickers


def _save_(tickers):
    """
    caches our list of ticker symbols locally
    :param tickers:
    :return:
    """
    with open(_screener_json_, 'w') as screener_json:
        json.dump(tickers, screener_json, 
                  indent=4, sort_keys=true)


TICKERS = _load_()
