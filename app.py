import os
import sys
import json
from datetime import datetime
from weather import Weather, Unit
from myconfig import *
import datetime as dt
import requests
from flask import Flask, request
import logging

logging.getLogger("requests").setLevel(logging.WARNING)

app = Flask(__name__)

#use same naming convention, the best choice is to use this standarized in PEP8. However do not mix: methodname with method_name, where the second one is much better than the first one.
#Try to use oop concept across all the bot's code.
#think about making some methods "private"; saying that I want to suggest you to name methods in that way: _private_method_()
#such a method is accessible but a developer which will use it, will be warned that he or she uses "internal API method".

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


def bustohome(user_id):
    #those arrays below should be rewritten to "mathematical" form so as loops and arrays. 
    #If really need to keep it in that way, make them global.
    
    hours = [5,6,6,7,8,9,9,10,11,11,12,13,13,14,15,15,16,17,17,18]
    mins = [55,30,55,45,30,15,50,35,15,50,10,15,50,25,5,40,10,0,50,50]
    h=dt.datetime.now().hour+2
    m=dt.datetime.now().minute
    IsBusAvailable = False 

    for x in range(18):
        if h == hours[x] and m <= mins[x] and mins[x] <= 9:
            send_message(user_id, "The earliest bus to home: " + str(hours[x]) + ":0" + str(mins[x]))
            IsBusAvailable=True            
            break
        if h == hours[x] and m <= mins[x] and mins[x] > 9:
            send_message(user_id, "The earliest bus to home: " + str(hours[x]) + ":" + str(mins[x]))
            IsBusAvailable=True
            break
        elif h < hours[x] and mins[x] <= 9:
            send_message(user_id, "The earliest bus to home: " + str(hours[x]) + ":0" + str(mins[x]))
            IsBusAvailable=True
            break
        elif h < hours[x] and mins[x] > 9:
            send_message(user_id, "The earliest bus to home: " + str(hours[x]) + ":" + str(mins[x]))
            IsBusAbailable=True
            break
        else:
            continue
        
    if(IsBusAvailable == False):
        send_message(user_id, "No more upcoming buses to home today!")

def bustolomza(user_id):
    hours = [6,7,7,8,9,10,10,11,12,13,13,14,14,15,16,17,18,18]
    mins = [22,2,52,52,37,22,47,27,37,7,32,27,52,27,17,12,17,57]#as written above^ do _NOT_ duplicate code.
    h=dt.datetime.now().hour+2
    m=dt.datetime.now().minute
    IsBusAvailable = False

    for x in range(18):
        if h == hours[x] and m <= mins[x] and mins[x] <= 9:
            send_message(user_id, "The earliest bus to lomza: " + str(hours[x]) + ":0" + str(mins[x]))
            IsBusAvailable = False
            break
        if h == hours[x] and m <= mins[x] and mins[x] > 9:
            send_message(user_id, "The earliest bus to lomza: " + str(hours[x]) + ":" + str(mins[x]))
            IsBusAvailable = False
            break
        elif h < hours[x] and mins[x] <= 9:
            send_message(user_id, "The earliest bus to lomza: " + str(hours[x]) + ":0" + str(mins[x]))
            IsBusAvailable = False
            break
        elif h < hours[x] and mins[x] > 9:
            send_message(user_id, "The earliest bus to lomza: " + str(hours[x]) + ":" + str(mins[x]))
            IsBusAvailable = False
            break
        else:
            continue

    if(IsBusAvailable == False):
        send_message(user_id, "No more upcoming buses to lomza today!")     
        

def weatherinfo(user_id):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_latlng(53.1780600,22.0593500)
    condition = location.condition
    forecasts = location.forecast

    currentTemp = ("Current temp is: " + str(condition.temp))
    send_message(user_id, currentTemp)
    
    for forecast in forecasts:
        send_message(user_id, forecast.text)
        
        highestTemp = ("Highest temperature today is: " + str(forecast.high))
        lowestTemp = ("Lowest temperature today is: " + str(forecast.low))
        
        send_message(user_id, highestTemp)
        send_message(user_id, lowestTemp)
        break

def nextlesson(user_id):
    dt.datetime.today()
    currentDay = dt.datetime.today().weekday()
    
    currentHour = dt.datetime.now().hour+2
    currentMinute = dt.datetime.now().minute
    IsLessonUpcoming = False


    for x in range(8):
        if currentHour < lessonHour[x] and lesson[currentDay][x] != "NULL" or currentHour == lessonHour[x] and currentMinute < lessonMinute[x]:
            IsLessonUpcoming = True
            lessonMessage = ("Next lesson: " + str(lesson[currentDay][x]))
            classMessage = ("In class: " + str(lessonClass[currentDay][x]))
            send_message(user_id, lessonMessage)
            send_message(user_id, classMessage)
            break
        else:
            continue

    if(IsLessonUpcoming == False):
        send_message(user_id, "No more lessons upcoming today!")

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    if message_text == "!weather":
                        weatherinfo(user_id=sender_id)
                    elif message_text == "!bus":
                        bustohome(user_id=sender_id)
                        bustolomza(user_id=sender_id)
                    elif message_text == "!lesson":
                        nextlesson(user_id=sender_id)
                    else:
                        send_message(sender_id, "Wrong command. Available commands: !weather, !bus, !lesson")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        msg = json.dumps(msg)
        print (u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)#is this needed on master branch? 
    #do NOT leave debug set to true on master aka production.
