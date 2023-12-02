import websocket # package name: websocket-client
import json
import threading
import time
import random

"""
Create a websocket to listen to the events a Discord bot can see
"""

# get token
from cfg import *

def sendRequest(ws, request):
    ws.send(json.dumps(request))

def recieveResponse(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(ws):
    payload = {"op":1,"d":"null"}
    sendRequest(ws, payload)
    print('Heartbeat sent')

def keepAlive(ws, interval):
    i = 1
    while True:
        time.sleep(interval/1000)
        print(f"Sending heartbeat {i}")
        i += 1
        heartbeat(ws)

# Connect
ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?encoding=json&v=10")

# Await first response, save interval
hello = recieveResponse(ws)
print(hello)
interval = hello['d']['heartbeat_interval']

# Send first heartbeat
#time.sleep((interval/1000)*random.random()) # "jitter" before first heartbeat, as per docs it's preferred but optional
heartbeat(ws)
print(recieveResponse(ws))

# Send auth
payload = {
    "op":2,
    "d":{
        "token":token,
        "intents":33281,
        "properties":{
            "os":"linux",
            "browser":"python-websocket-client",
            "device":"python-websocket-client"
        }
    }
}
sendRequest(ws, payload)
print(recieveResponse(ws)) # READY payload

# Start heartbeat
t2 = threading.Thread(target=keepAlive, args=(ws, interval))
t2.start()

# Listen for messages
while True:
    event = recieveResponse(ws)

    try:
        print(event)
    except:
        pass
