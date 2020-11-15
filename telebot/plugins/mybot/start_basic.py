import re
from telebot.plugins.mybot import *
from telethon import events, custom, Button
import heroku3
from telebot.telebotConfig import Var

LOAD_MYBOT = Var.LOAD_MYBOT
Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

# start-other-disabled


@tgbot.on(events.NewMessage(pattern="^/start"))
async def start_all(event):
    if event.sender_id == OWNER_ID:
        return
    else:
        await tgbot.send_message(event.chat_id,
                                 startotherdis,
                                 buttons=[
                                     (Button.url(
                                         "TeleBot",
                                         url="https://github.com/xditya/TeleBot"))]
                                 )

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
    await event.delete()
    await tgbot.send_message(event.chat_id,
                             "Here are the available options.",
                             buttons=[
                                 [custom.Button.inline("PM Bot", data="pmbot")],
                                 [Button.url(
                                     "Logs", url=f"https://t.me/{Var.TG_BOT_USER_NAME_BF_HER}?start=logs")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmbot")))
async def pmbot(event):
    await event.delete()
    await tgbot.send_message(event.chat_id,
                             f"Here are the availabe settings for PM bot.\nCurrently active: {LOAD_MYBOT}",
                             buttons=[
                                 [custom.Button.inline("Enable", data="enable"), custom.Button.inline("Disable", data="disable")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"enable"))
          )  # pylint: disable=oof
async def enable(event):
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


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"disable"))
          )  # pylint: disable=oof
async def enable(event):
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
