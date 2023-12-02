# sod-monitor

A Discord bot interface for monitoring a scraping formated reports from a channel.

# WIP

Current usage:

* Create a copy of `cfg.py.example` as `cfg.py` and do your configuration in that
* Run `python rq.py` to create `dump.py` of the configured channel from now back to the specified date
* Run `python parse.py` to print some preliminary data to stdout
