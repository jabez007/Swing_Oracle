import json


class AppSettings(dict):
    
	def __init__(self):
		with open('app.config') as json_data:
			for k, v in json.load(json_data).items():
				self[k] = v





