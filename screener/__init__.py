import json
import os


_screener_json_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'screener.json')

TICKERS = list()
with open(_screener_json_) as screener_json:
	TICKERS = json.load(screener_json)


def save():
	with open(_screener_json_, 'w') as screener_json:
		json.dump(TICKERS, screener_json, indent=4)