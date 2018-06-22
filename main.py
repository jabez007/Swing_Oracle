import data
from pprint import pprint

x, y = data.DAILY["PLUG"].get_input_output(20, 1)
pprint(x[0])
pprint(y[0])
