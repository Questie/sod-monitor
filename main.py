import os

from messageDB import *
from rq import *

mdb = messageDB()

for file in os.listdir('dumps'):
    print(f'dumps/{file}')
    with open(f'dumps/{file}') as f:
        exec(f.read())
        mdb.addDump(messageDump)

def rescrape(channel):
    if channel not in mdb.newestMessages:
        print('Unknown channel')
        return
    oldstamp = mdb.getNewestMessage(channel)['timestamp']
    dump = dumpChannel(channel, oldstamp)
    if dump != None:
        mdb.addDump(dump)

def scrape(channel, oldstamp='2023-11-30T21:00:00.000000+00:00'):
    dump = dumpChannel(channel, oldstamp)
    if dump != None:
        mdb.addDump(dump)
