# git+git://github.com/940094/twilio-python.git
# Download the helper library from https://www.twilio.com/docs/python/install
from flask import redirect, render_template, request, session
from twilio.rest import Client
import os, requests

print('running send_sms.py')

# twilio api
def send_sms(user, email, full_name):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body='New Lead:',
            from_='+18432024359',
            to=user['phone'])

    print(message.sid)
    return ('', 400)

send_sms({'phone': '+18435555555'}, 'email@email.com', 'John Smith')


'''
# TILL api
# TILL_URL = os.environ.get("TILL_URL")
def send_sms(user, email, full_name):
    result = requests.post(TILL_URL, json={
        "phone": ["18434250626"],
        "questions" : [{
            "text": "You have a new lead:",
            "tag": "favorite_color",
            "responses": ["Red", "Green", "Yellow"],
            "webhook": "https://yourapp.herokuapp.com/results/"
        }],
        "conclusion": "Thank you for your time"
    })
    #print(result)
    return ('', 203)

send_sms('1','1','1')
'''
