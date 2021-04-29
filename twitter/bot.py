'''----------------------------------------------------------------------------
Name:        Twitter Bot (bot.py)
Purpose:     A script that sends out a tweet containing general coronavirus 
             statistics from the Government of Ontario. Script is called 
             through heroku scheduler at 11:00AM every day.

Author:      Nicholas Chong
Created:     2020-06-19 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import urllib.request
import pprint
import json
from . import tweets 
from datetime import datetime

def main(today):
    if today.date != datetime.today().date():
        return print('ERROR: The record date does not match todays date')

    # Send out the daily update tweet
    tweets.daily_update(
        today.date, 
        today.new_cases, 
        today.total_cases,
        today.new_tests,
    )
