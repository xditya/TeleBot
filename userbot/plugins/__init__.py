# inspired by https://github.com/sandy1709/catuserbot/blob/master/userbot/plugins/__init__.py

import os
import re
import time
import math
import heroku3
import requests
from heroku_config import Var
from userbot import telever
from userbot.uniborgConfig import Config
from telethon import events
from datetime import datetime

Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Var.HEROKU_APP_NAME
HEROKU_API_KEY = Var.HEROKU_API_KEY

def check(tele):
    if "/start" in tele:
        return True
    wew = re.search(re.escape(f"\\b{tele}\\b"), "a|b|c|d")
    if wew:
        return True
    return False

# inspired by https://github.com/sandy1709/catuserbot/blob/master/userbot/plugins/__init__.py
# @sn12384

async def telealive():
    start = datetime.now()
    if Config.SUDO_USERS:
        sudo = "Active"
    else:
        sudo = "Disabled"
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    try:
        useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/80.0.3987.149 Mobile Safari/537.36'
                     )
        user_id = Heroku.account().id
        headers = {
            'User-Agent': useragent,
            'Authorization': f'Bearer {Var.HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        result = r.json()
        quota = result['account_quota']
        quota_used = result['quota_used']

        # Used
        remaining_quota = quota - quota_used
        math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)

        # Current
        App = result['apps']
        try:
            App[0]['quota_used']
        except IndexError:
            AppQuotaUsed = 0
        else:
            AppQuotaUsed = App[0]['quota_used'] / 60
            math.floor(App[0]['quota_used'] * 100 / quota)

        hrs = math.floor(AppQuotaUsed / 60)
        mins = math.floor(AppQuotaUsed % 60)
        dyno = f"{hrs}h {mins}m/{hours}h {minutes}m"
    except Exception as e:
        dyno = e
    info = f"TeleBot Stats\
                  \n\nVersion : {telever}\
                  \nSudo : {sudo}\
		  \nPing : {ms}\
                  \nDyno : {dyno}\
                  "
    return info
