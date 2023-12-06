import requests
import json
import time
import datetime

# get token
from cfg import *
header     = {"Authorization": f'Bot {token}', "Content-Type": "application/json"}

def dumpChannel(channel_id, oldstamp=False, delay=2, limit=100):
    """Dumps every message from the latest one in channel channel_id back to time oldstamp into a file"""
    # delay = 2 # 1 second seems like a good value to not trigger the rate-limits. YMMV
    # limit = 100 # how many messages to get at once
    if not oldstamp:
        print('No end point avoiding full dump')
        return

    # Get channel data
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    r = requests.get(url, headers=header)
    if r.text == '{"message": "Unknown Channel", "code": 10003}':
        print(f'Channel {channel_id} does not exist!')
        return
    # Iterator for the before paramter
    ch = json.loads(r.text)
    message_id = ch['last_message_id']
    channel_name = ch['name']
    print(f'Channel {channel_id} exists and is called: {channel_name}\nSleeping {delay} seconds. Ratelimit: {r.headers["x-ratelimit-remaining"]}. Reset: {r.headers["x-ratelimit-reset-after"]}')
    time.sleep(delay)

    # Get latest message so we have a message ID to start with
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
    r = requests.get(url, headers=header)
    messageDump = [json.loads(r.text)]

    print(f'Got latest message. Sleeping {delay} seconds. Ratelimit: {r.headers["x-ratelimit-remaining"]}. Reset: {r.headers["x-ratelimit-reset-after"]}')
    time.sleep(delay)

    # Return condition
    reached_oldstamp = False

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
    with open(f'dumps/dump-{channel_name}-{datetime.datetime.now().isoformat()}.py', 'w') as f:
        print(f'messageDump = {messageDump}', file=f)
    return messageDump

def dumpForumChannel(channel_ids, oldstamp=False, delay=2, limit=100):
    """TODO"""
    # f"https://discord.com/api/v10/guilds/263036731165638656/threads/active"
    # f"https://discord.com/api/v10/channels/{channel_id}/threads/archived/public"
    pass
