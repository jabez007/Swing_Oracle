import configuration_manager
import json
import os
import requests


_screener_path_ = os.path.dirname(os.path.realpath(__file__))
_screener_json_ = os.path.join(_screener_path_, 'screener.json')


def _load_(tickers=list()):
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
    _download_(tickers)
    _save_(tickers)
    return tickers


def _download_(tickers, page=1):
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
    with open(_screener_json_, 'w') as screener_json:
        json.dump(tickers, screener_json, indent=4)


TICKERS = _load_()
