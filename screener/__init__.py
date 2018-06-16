import json
import os


_screener_path_ = os.path.dirname(os.path.realpath(__file__))
_screener_json_ = os.path.join(_screener_path_, 'screener.json')
TICKERS = list()


def load():
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
    save()


"""
with open(_screener_json_) as screener_json:
    TICKERS = json.load(screener_json)
"""


def save():
    with open(_screener_json_, 'w') as screener_json:
        json.dump(TICKERS, screener_json, indent=4)


load()
