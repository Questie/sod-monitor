import requests
import json
import time
import datetime

# get token, channel_id, and oldstamp
from cfg import *

"""
Dumps every message from the latest one in channel channel_id back to time oldstamp into a file
"""

header     = {"Authorization": f'Bot {token}', "Content-Type": "application/json"}
delay      = 2 # 1 second seems like a good value to not trigger the rate-limits. YMMV
limit      = 100 # how many messages to get at once

# Get latest message so we have a message ID to start with
url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=1"
r = requests.get(url, headers=header)
newest_message = json.loads(r.text)[0]
messageDump = [newest_message]

print(f'Got latest message. Sleeping {delay} seconds.')
time.sleep(delay)

# Return condition
reached_oldstamp = False
# Iterator for the before paramter
message_id = newest_message['id']

while not reached_oldstamp:
    # Get message batch
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}&before={message_id}"
    r = requests.get(url, headers=header)
    messages = json.loads(r.text)
    # Check timestamp and add to dump
    for message in messages:
        message_id = message['id']
        # Timestamp reached?
        if oldstamp > message['timestamp']:
            reached_oldstamp = True
            break
        messageDump.append(message)
    # Rate limiting
    if not reached_oldstamp:
        reset = delay
        remaining =  r.headers['x-ratelimit-remaining']
        if remaining == '0':
            reset = float(r.headers['x-ratelimit-reset-after'])
        print(f'Added more messages, now {len(messageDump)}. Sleeping {reset} seconds. Ratelimit: {remaining}. Reset: {r.headers["x-ratelimit-reset-after"]}.')
        time.sleep(reset)

print(f'Done. Added {len(messageDump)} messages.')

# Dump messages to file
with open('dump.py', 'w') as f:
    print(f'messageDump = {messageDump}', file=f)
