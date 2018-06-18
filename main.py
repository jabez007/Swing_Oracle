import data
import json
import oracle
from pprint import pprint
import screener

X, y = oracle.format_daily_data(data.DAILY)

pprint(X)
print(len(X))
