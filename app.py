from flask import Flask
from flask import request
import json
import requests
import pandas as pd
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from service.chatBotService import find_local_and_people

# from twilio.rest import Client
#
# account_sid = 'AC9530ac7f6cd21d8e0321c0df0d83e5ed'
# auth_token = '2cfba3a04e800b40eed3377fcc518371'
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#     from_='whatsapp:+14155238886',
#     body='Your appointment is coming up on July 21 at 3PM',
#     to='whatsapp:+556292054862'
# )
#
# print(message.sid)


# initializing chatbot
authenticator = IAMAuthenticator('W30jmk_PvRlI0AuFrr4Y0f4lOWxBqXEuT4eDjA9QtfWQ')
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/f9baf793-cfc3-4e9b-a0d4-67fc3db16b45')
# creating a chatbot session
chatbot_session = assistant.create_session(
    assistant_id='7fdda5d1-75d5-4b16-8201-925b0a64e674'
).get_result()
#print(chatbot_session)
# initializing flask
app = Flask(__name__)


# Falta achar algum jeito de transformar todos os nomes, responsaveis e talvez blocos em csv para upar no watson como entidade

# HTML Requests
@app.route('/send_message', methods=['GET'])
def send_message():
    user_message = request.get_json()['user_message']  # getting the user message

    print('mensagem do usario: ' + user_message)


    # getting the bot answer
    response = assistant.message(
        assistant_id='7fdda5d1-75d5-4b16-8201-925b0a64e674',
        session_id=chatbot_session['session_id'],
        input={
            'message_type': 'text',
            'text': user_message
        }).get_result()
    print(response)


    if (response['output']['intents'][0]['intent'] == 'Ramal' and response['output']['entities']):
        #return findContact(response['output']['entities'])
        return find_local_and_people(response['output']['entities'])
    return 'ok'


# running app
if __name__ == '__main__':
    app.run()
