import json


AppSettings = dict()
with open('app.config') as json_data:
    for k, v in json.load(json_data).items():
        AppSettings[k] = v
