import re
from telebot.plugins.mybot import *
from telethon import events, custom, Button
import heroku3
from telebot import telebotConfig
import asyncio
import os
import requests

LOAD_MYBOT = Var.LOAD_MYBOT
Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

# start-other-disabled


@tgbot.on(events.NewMessage(pattern="^/start (.*)"))
async def start_all(event):
    if event.sender_id == OWNER_ID:
        return
    else:
        await tgbot.send_message(event.chat_id,
                                 startotherdis,
                                 buttons=[(custom.Button.inline("What can I do here?", data="oof"))]
                                 )
    try:
        hmm = event.pattern_match.group(1)
    except BaseException:
        pass
    if hmm == "logs":
        with open('logs.txt', 'w') as log:
            log.write(app.get_log())
        ok = app.get_log()
        url = "https://del.dog/documents"
        r = requests.post(url, data=ok.encode("UTF-8")).json()
        url = f"https://del.dog/{r['key']}"
        if event.sender_id == OWNER_ID:
            await tgbot.send_file(
                event.chat_id,
                "logs.txt",
                reply_to=event.id,
                caption="**Heroku** TeleBot Logs",
                buttons=[
                    [Button.url("View Online", f"{url}")],
                    [Button.url("Crashed?", "t.me/TeleBotHelpChat")]
                ])
        else:
            await tgbot.send_message(event.chat_id, "This option is only for my owner!")
        await asyncio.sleep(5)
        return os.remove('logs.txt')


# start-owner


@tgbot.on(events.NewMessage(pattern="^/start", from_users=OWNER_ID))
async def owner(event):
    await tgbot.send_message(event.chat_id,
                             startowner,
                             buttons=[
                                 [Button.url("Support",
                                             url="https://t.me/TeleBotSupport")],
                                 [custom.Button.inline(
                                     "Settings ⚙️", data="settings")]
                             ])

# callbacks


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"settings")))
async def settings(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "Here are the available options.",
                                 buttons=[
                                     [custom.Button.inline("PM Bot", data="pmbot")],
                                     [Button.url(
                                         "Logs", url=f"https://t.me/{Var.TG_BOT_USER_NAME_BF_HER}?start=logs")]
                                 ])
    else:
        await event.answer("You cant use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmbot")))
async def pmbot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 f"Here are the availabe settings for PM bot.\nCurrently active: {LOAD_MYBOT}",
                                 buttons=[
                                     [custom.Button.inline("Enable", data="enable"), custom.Button.inline("Disable", data="disable")]
                                 ])
    else:
        await event.answer("You cant use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"enable"))
          )  # pylint: disable=oof
async def enable(event):
    if event.sender_id == OWNER_ID:
        telebot = "LOAD_MYBOT"
        if Var.HEROKU_APP_NAME is not None:
            app = Heroku.app(Var.HEROKU_APP_NAME)
        else:
            mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        heroku_var = app.config()
        heroku_var[telebot] = "True"
        mssg = "Successfully turned on PM Bot. Restarting now, please give me a minute."
        await event.delete()
        await tgbot.send_message(event.chat_id, mssg)
    else:
        await event.answer("You cant use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"disable"))
          )  # pylint: disable=oof
async def enable(event):
    if event.sender_id == OWNER_ID:
        telebot = "LOAD_MYBOT"
        if Var.HEROKU_APP_NAME is not None:
            app = Heroku.app(Var.HEROKU_APP_NAME)
        else:
            mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
            return
        heroku_var = app.config()
        heroku_var[telebot] = "False"
        mssg = "Successfully turned off PM Bot. Restarting now, please give me a minute."
        await event.delete()
        await tgbot.send_message(event.chat_id, mssg)
    else:
        await event.answer("You cant use this bot.", alert=True)
