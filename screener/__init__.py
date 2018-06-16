import configuration_manager
import json
import os
import requests


_screener_path_ = os.path.dirname(os.path.realpath(__file__))
_screener_json_ = os.path.join(_screener_path_, 'screener.json')
TICKERS = list()


def _load_():
    for f in os.listdir(_screener_path_):
        if f.endswith(".json"):
            with open(os.path.join(_screener_path_, f)) as f_json:
                data = json.load(f_json)
            if "data" not in data:
                TICKERS.extend(data)
            else:
                for d in data["data"]:
                    if not any(d["ticker"] == t["ticker"] for t in TICKERS):
                        TICKERS.append(d)
    _download_()
    _save_()


def _download_(page=1):
    r = requests.get("https://api.intrinio.com/securities/search?conditions=52_week_low~gte~1.00,52_week_high~lte~25.00,marketcap~gte~300000000,marketcap~lte~2000000000,average_daily_volume~gte~500000&page_number=" + str(page),
                     auth=(configuration_manager.AppSettings["intrinio"]["api username"],
                           configuration_manager.AppSettings["intrinio"]["api password"]))

    data = r.json()
    for d in data["data"]:
        if not any(d["ticker"] == t["ticker"] for t in TICKERS):
            TICKERS.append(d)

    if page < data["total_pages"]:
        _download_(page+1)


def _save_():
    with open(_screener_json_, 'w') as screener_json:
        json.dump(TICKERS, screener_json, indent=4)


_load_()
