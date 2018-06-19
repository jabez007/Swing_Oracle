import data
import oracle
from pprint import pprint

X, y = oracle.format_daily_data(data.DAILY)

pprint(X)
print(len(X))
