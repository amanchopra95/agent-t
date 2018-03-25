import json
import requests

url = "https://www.googleapis.com/customsearch/v1"
key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cx = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def get_request(parameter):
	if parameter['geo-state-us']:
		query=parameter['geo-state-us']
	elif parameter['geo-country']:
		query = parameter['geo-country']
	elif parameter['geo-city']:
		query = parameter['geo-city']
	else:
		query = parameter['destination']

	parameters = {
	'key' : key,
    'cx' : cx,
    'q' : query,
    }
	r = requests.get(url, params = parameters)
	data = r.json()
	reply = data['items']

	return reply








#https://www.googleapis.com/customsearch/v1