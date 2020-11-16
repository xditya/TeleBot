import re
from telebot.plugins.mybot import *
from telethon import events, custom, Button
import heroku3
import asyncio
import os
import requests
from telebot.plugins.mybot.sql.blacklist_sql import all_bl_users()
from telebot.plugins.mybot.sql.users_sql import all_users()

LOAD_MYBOT = Var.LOAD_MYBOT
Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

# start-other-disabled


@tgbot.on(events.NewMessage(pattern="^/start"))  # pylint: disable=oof
async def start_all(event):
    if event.sender_id == OWNER_ID and LOAD_MYBOT == "True":
        return
    else:
        await tgbot.send_message(event.chat_id,
                                 startotherdis,
                                 buttons=[(custom.Button.inline("What can I do here?", data="wew"))]
                                 )

# start-owner


@tgbot.on(events.NewMessage(pattern="^/start",
                            from_users=OWNER_ID))  # pylint: disable=oof
async def owner(event):
    await tgbot.send_message(event.chat_id,
                             startowner,
                             buttons=[
                                 [Button.url("Support",
                                             url="https://t.me/TeleBotSupport")],
                                 [custom.Button.inline(
                                     "Settings ⚙️", data="settings")],
                                 [custom.Button.inline(
                                     "Stats ⚙️", data="stats")]
                             ])


@tgbot.on(events.NewMessage(pattern="^/start logs", from_users=OWNER_ID))
async def logs(event):
    try:
        Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
        app = Heroku.app(Var.HEROKU_APP_NAME)
    except BaseException:
        await tgbot.send_message(event.chat_id, " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku var !")
        return
    with open('logs.txt', 'w') as log:
        log.write(app.get_log())
    ok = app.get_log()
    url = "https://del.dog/documents"
    r = requests.post(url, data=ok.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    await tgbot.send_file(
        event.chat_id,
        "logs.txt",
        reply_to=event.id,
        caption="**Heroku** TeleBot Logs",
        buttons=[
            [Button.url("View Online", f"{url}")],
            [Button.url("Crashed?", "t.me/TeleBotHelpChat")]
        ])
    await asyncio.sleep(5)
    return os.remove('logs.txt')


# callbacks


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"wew"))
          )  # pylint: disable=oof
async def settings(event):
    await event.delete()
    await tgbot.send_message(event.chat_id,
                             "There isn't much that you can do over here rn.",
                             buttons=[
                                     [Button.url(
                                         "Repository", url="https://github.com/xditya/TeleBot")],
                                     [Button.url(
                                         "Support", url="https://t.me/TeleBotSupport")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"settings"))
          )  # pylint: disable=oof
async def settings(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "Here are the available options.",
                                 buttons=[
                                     [custom.Button.inline(
                                         "PM Bot", data="pmbot")],
                                     [Button.url(
                                         "Logs", url=f"https://t.me/{Var.TG_BOT_USER_NAME_BF_HER}?start=logs")]
                                 ])
    else:
        await event.answer("You cant use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"settings"))
          )  # pylint: disable=oof
async def settings(event):
    if event.sender_id == OWNER_ID:
        allu = all_users()
        blu = all_bl_users()
        pop = "Here is the stats for your bot:\nTotal Users = {}\nBlacklisted Users = {}".format(
            allu, blu)
        await event.answer(pop, alert=True)
    else:
        await event.answer("You cant use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmbot"))
          )  # pylint: disable=oof
async def pmbot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 f"Here are the availabe settings for PM bot.\nCurrently active: {LOAD_MYBOT}",
                                 buttons=[
                                     [custom.Button.inline("Enable", data="enable"), custom.Button.inline(
                                         "Disable", data="disable")]
                                 ])
    else:
        await event.answer("You cant use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"enable"))  # pylint: disable=oof
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
