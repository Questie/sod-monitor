# sod-monitor

A Discord bot interface for monitoring and scraping formated reports from a channel.

# WIP

Current usage:

* Create a copy of `cfg.py.example` as `cfg.py` and configure your Discord bot token in that
* Run `python` (or your interpreter of choice)
* Enter `from main import *`
* Use `scrape('channel_id')` or `rescrape('channel_id')` to get new messages
    * `'channel_id'` is a numerical Discord ID for the channel, enclosed by single quotes (has to be string type)
* Interact with the `mdb.objectDB` dict and it's children `quests`, `npcs`, and `objects` to get the information
