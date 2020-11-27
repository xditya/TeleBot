#    TeleBot - UserBot
#    Copyright (C) 2020 TeleBot

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
from telebot.plugins.mybot import *
from telethon import events, Button
import heroku3
import asyncio
import os
import requests
from telebot.plugins.mybot.sql.blacklist_sql import all_bl_users
from telebot.plugins.mybot.sql.users_sql import all_users
from telebot.plugins import TELE_NAME
from telebot.plugins.mybot.sql.userbase_sql import add_to_userbase, present_in_userbase, full_userbase
from datetime import datetime
from telethon import events
from telebot.telebotConfig import Var

##################--CONSTANTS--##################
LOAD_MYBOT = Var.LOAD_MYBOT
Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
################--CONSTANTS-END-#################

# start-others


@tgbot.on(events.NewMessage(pattern="^/start"))  # pylint: disable=oof
async def start_all(event):
    if event.chat_id == OWNER_ID:
        return
    target = event.sender_id
    if present_in_userbase(target):
        pass
    else:
        try:
            add_to_userbase(target)
        except BaseException:
            pass
    if LOAD_MYBOT == "False":
        await tgbot.send_message(event.chat_id,
                                 startotherdis,
                                 buttons=[
                                     (Button.inline(
                                         "What can I do here?",
                                         data="wew"))]
                                 )
    elif LOAD_MYBOT == "True":
        await tgbot.send_message(event.chat_id,
                                 startotherena,
                                 buttons=[
                                     [Button.url(
                                         "TeleBot", url="https://github.com/xditya/TeleBot")],
                                     [Button.inline(
                                         "Whats this?", data="telebot")]
                                 ]
                                 )

# start-owner


@tgbot.on(events.NewMessage(pattern="^/start",
                            from_users=OWNER_ID))  # pylint: disable=oof
async def owner(event):
    await tgbot.send_message(event.chat_id,
                             startowner,
                             buttons=[
                                 [Button.inline(
                                     "Settings ⚙️", data="settings"),
                                  Button.inline(
                                     "Stats ⚙️", data="stats")],
                                 [Button.inline("Broadcast",
                                                data="telebroad")],
                                 [Button.url("Support",
                                             url="https://t.me/TeleBotSupport")]
                             ])


@tgbot.on(events.NewMessage(pattern="^/start logs",
                            from_users=OWNER_ID))  # pylint: disable=oof
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
                                     [Button.inline(
                                         "Deploy me for yourself", data="deployme")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"telebot"))
          )  # pylint: disable=oof
async def settings(event):
    await event.delete()
    await tgbot.send_message(event.chat_id,
                             f"This is the personal help bot of {TELE_NAME}. You can contact me using this bot if necessary, or if I missed out your PM.",
                             buttons=[
                                     [Button.inline(
                                         "Deploy me for yourself", data="deployme")]
                             ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deployme"))
          )  # pylint: disable=oof
async def settings(event):
    await event.edit("Browse through the available options:",
                     buttons=[
                         [(Button.url("Repository", url="https://github.com/xditya/TeleBot")),
                          (Button.url("Deploy", url="https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot%2F&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot"))],
                         [Button.url("Support",
                                     url="https://t.me/TeleBotSupport")]
                     ])


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"settings"))
          )  # pylint: disable=oof
async def settings(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "Here are the available options.",
                                 buttons=[
                                     [Button.inline(
                                         "PM Bot", data="pmbot")],
                                     [Button.url(
                                         "Logs", url=f"https://t.me/{Var.TG_BOT_USER_NAME_BF_HER}?start=logs")]
                                 ])
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats"))
          )  # pylint: disable=oof
async def settings(event):
    if event.sender_id == OWNER_ID:
        allu = len(all_users())
        blu = len(all_bl_users())
        pop = "Here is the stats for your bot:\nTotal Users = {}\nBlacklisted Users = {}".format(
            allu, blu)
        await event.answer(pop, alert=True)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmbot"))
          )  # pylint: disable=oof
async def pmbot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 "Here are the availabe settings for PM bot.",
                                 buttons=[
                                     [Button.inline("Enable/Disable", data="onoff"), Button.inline(
                                         "Custom Message", data="cmssg")]
                                 ])
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"onoff"))
          )  # pylint: disable=oof
async def pmbot(event):
    if event.sender_id == OWNER_ID:
        await event.delete()
        await tgbot.send_message(event.chat_id,
                                 f"Turn the PM bot on or off.\nCurrently enabled: {LOAD_MYBOT}",
                                 buttons=[
                                     [Button.inline("Enable", data="enable"), Button.inline(
                                         "Disable", data="disable")]
                                 ])
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"cmssg"))
          )  # pylint: disable=oof
async def custom(event):
    if event.sender_id == OWNER_ID:
        await event.reply("You can change your PMBot start message here.\nSend the message you want to display when someone started the bot, /cancel to cancel the operation.")
        async with event.client.conversation(OWNER_ID) as conv:
            response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
            response = await response
            themssg = response.message.message
            if themssg == "/cancel":
                await tgbot.send_message(event.chat_id, "Operation Cancelled.")
                return
            telebot = "PMBOT_START_MSSG"
            if Var.HEROKU_APP_NAME is not None:
                app = Heroku.app(Var.HEROKU_APP_NAME)
            else:
                mssg = "`**HEROKU**:" "\nPlease setup your` **HEROKU_APP_NAME**"
                return
            heroku_var = app.config()
            heroku_var[telebot] = f"{themssg}"
            mssg = "Changed the PMBot start message!!\n**Restarting now**, please give me a minute."
            await event.delete()
            await tgbot.send_message(event.chat_id, mssg)
    else:
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"enable"))
          )  # pylint: disable=oof
async def enablee(event):
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
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"disable"))
          )  # pylint: disable=oof
async def dissable(event):
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
        await event.answer("You can't use this bot.", alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"telebroad"))
          )  # pylint: disable=oof
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        await event.answer("You can't use this bot")
        return
    await tgbot.send_message(event.chat_id, "Send the message you want to broadcast!\nSend /cancel to stop.")
    async with event.client.conversation(OWNER_ID) as conv:
        response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
        response = await response
        themssg = response.message.message
    if themssg is None:
        await tgbot.send_message(event.chat_id, "An error has occured...")
    if themssg == "/cancel":
        await tgbot.send_message(event.chat_id, "Broadcast cancelled!")
        return
    targets = full_userbase()
    users_cnt = len(full_userbase())
    err = 0
    success = 0
    lmao = await tgbot.send_message(event.chat_id, "Starting broadcast to {} users.".format(users_cnt))
    start = datetime.now()
    for ok in targets:
        try:
            await tgbot.send_message(int(ok.chat_id), themssg)
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            err += 1
            try:
                await tgbot.send_message(Var.PRIVATE_GROUP_ID, f"**Error**\n{str(e)}\nFailed for user: {chat_id}")
            except BaseException:
                pass
    end = datetime.now()
    ms = (end - start).seconds
    done_mssg = """
Broadcast completed!\n
Sent to `{}` users in `{}` seconds.\n
Failed for `{}` users.\n
Total users in bot: `{}`.\n
""".format(success, ms, err, users_cnt)
    await lmao.edit(done_mssg)
    try:
        await tgbot.send_message(Var.PRIVATE_GROUP_ID, f"#Broadcast\nCompleted sending a broadcast to {success} users.")
    except BaseException:
        await tgbot.send_message(event.chat_id, "Please add me to your Private log group for proper use.")
