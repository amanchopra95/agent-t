from flask import Flask, request
from pymessenger import Bot
from utils import fetch_reply
import requests, json
import os

app = Flask("app")

FB_ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "HELLO123"

@app.route('/', methods=['GET'])
def verify():
	if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
		if not request.args.get('hub.verify_token') == VERIFICATION_TOKEN:
			return "Verification token invalid", 403
		return request.args['hub.challenge'], 200
	return "Hello, World", 200

@app.route('/', methods=['POST'])
def webhook():
	print(request.data)
	data = request.get_json()

	if data['object'] == "page":
		entries = data["entry"]

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):

					if messaging_event['message'].get('text'):

						msg = messaging_event['message']['text']

						if msg == "button":
							button = [{"type" : "web_url",
										"url" : "www.facebook.com/coolaman95",
										"title" : "Developer"}]
							bot.send_button_message(sender_id, "Check this out !!", button)

							return "ok", 200
						if messaging_event['message'].get('quick_reply'):
							payload = messaging_event['message']['quick_reply']['payload']
							msg = payload

						reply = fetch_reply(msg, sender_id)
						
						if reply['type'] == 'trip':
							print("Sending message trip")
							print(reply['data'])
							bot.send_generic_message(sender_id, reply['data'])
							print("Message sent")
						elif reply['type'] == 'none':
							print("Sending message none")
							bot.send_text_message(sender_id, reply['data'])
						else:
							print("sending message else")
							bot.send_text_message(sender_id, reply['data'])
							print("message sent")
						
				elif messaging_event.get('postback'):
					payload = messaging_event['postback']['payload']
					if payload == 'destination':
						reply = "Where do you want to go ?"
						bot.send_text_message(sender_id, reply)
					elif payload == 'get_started':
						bot.send_text_message(sender_id, "Tell us where do you want to go ?")

	return "ok", 200

def set_greeting_text():
	headers = {
		'Content-Type':'application/json'
		}
	data = {
		"setting_type":"greeting",
		"greeting":{
			"text":"Hi {{user_first_name}}! I am your Travel agent."
			}
		}
	ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
	r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
	print(r.content)

def set_persistent_menu():
	headers = {
			'content-Type' : 'application/json'
	}

	data = {
			"setting_type" : "call_to_actions",
			"thread_state" : "existing_thread",
			"call_to_actions" : [
					{
							"type" : "postback",
							"title" : "Destination",
							"payload" : "destination",
					},
					{
							"type" : "postback",
							"title" : "Get Started",
							"payload" : "get_started",
					}
			]
	}

	ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
	r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
	print(r.content)

set_greeting_text()
set_persistent_menu()


if __name__ == '__main__':
	app.run(port=8080, debug=True, use_reloader=True)
