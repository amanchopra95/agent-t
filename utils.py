import apiai
import json
import requests
from scrap import get_request

APIAI_ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bot = apiai.ApiAI(APIAI_ACCESS_TOKEN)

def api_response(query, sender_id):
	req = bot.text_request()
	req.lang = 'en'
	req.session_id = sender_id
	req.query = query
	response = req.getresponse()
	return json.loads(response.read().decode('utf-8'))


def parse_response(response):
	result = response['result']
	parameters = result.get('parameters')
	intent = result['metadata'].get('intentName')
	return intent, parameters



def fetch_reply(query, sender_id):
	response = api_response(query, sender_id)
	print(response)
	intent, parameters = parse_response(response)

	reply = {}

	if response['result']['action'].startswith('smalltalk'):
		reply['type'] = 'smalltalk'
		reply['data'] = response['result']['fulfillment']['speech']

	elif intent == "trip":
		reply['type'] = 'trip'
		items = get_request(parameters)

		print(items)

		elements = []
		count = 0

		for item in items:
			if count <= 5:
				element = {}
				element['title'] = item['title']
				element['item_url'] = item['link']
				element['image_url'] = item['pagemap']['cse_thumbnail'][0]['src']
				print(element['item_url'])
				print(element['title'])
				print(element['image_url'])
				element['buttons'] = [{
						"type" : "web_url",
						"title" : "Book Now",
						"url" : item['link'],
				}]

				elements.append(element)
				count+=1
				
		reply['data'] = elements

	else:
		reply['type'] = 'none'
		reply['data'] = [{"type": "web_url",
                          "payload": "SHOW_HELP",
                          "title": "Click here for help!"}]
	print(reply)
	return reply



