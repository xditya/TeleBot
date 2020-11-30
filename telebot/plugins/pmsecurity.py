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

import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import telebot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telebot import ALIVE_NAME, CMD_HELP, CUSTOM_PMPERMIT, bot
from telebot.utils import admin_cmd

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
TELEPIC = (
    PMPERMIT_PIC
    if PMPERMIT_PIC
    else "https://telegra.ph/file/92cfbab6598148837c2e4.jpg"
)
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
myid = bot.uid
MESAG = (
    str(CUSTOM_PMPERMIT)
    if CUSTOM_PMPERMIT
    else "`TeleBot PM security! Please wait for me to approve you. 😊"
)
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot User"
USER_BOT_WARN_ZERO = "`I had warned you not to spam. Now you have been blocked and reported until further notice.`\n\n**GoodBye!** "
USER_BOT_NO_WARN = (
    "**PM Security ~ TeleBot**\n\nNice to see you here, but  "
    "[{}](tg://user?id={}) is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**You have** `{}/{}` **warnings...**"
    "\n\n   ~ Thank You."
)


@telebot.on(admin_cmd(pattern="a ?(.*)"))
@telebot.on(admin_cmd(pattern="approve ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id in PM_WARNS:
                del PM_WARNS[chat.id]
            if chat.id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat.id].delete()
                del PREV_REPLY_MESSAGE[chat.id]
            pmpermit_sql.approve(chat.id, reason)
            await event.edit(
                "Approved [{}](tg://user?id={}) to PM you.".format(firstname, chat.id)
            )
            await asyncio.sleep(3)
            await event.delete()


# Approve outgoing


@bot.on(events.NewMessage(outgoing=True))
async def you_dm_niqq(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id not in PM_WARNS:
                pmpermit_sql.approve(chat.id, "outgoing")
                logit = "#Auto_Approved\nUser - [{}](tg://user?id={})".format(
                    chat.first_name, chat.id
                )
                try:
                    await borg.send_message(Var.PRIVATE_GROUP_ID, logit)
                except BaseException:
                    pass


@telebot.on(admin_cmd(pattern="block ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 719195224:
            await event.edit("You tried to block my master. GoodBye for 100 seconds! 💤")
            await asyncio.sleep(100)
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "Get lost retard.\nBlocked [{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))


@telebot.on(admin_cmd(pattern="da ?(.*)"))
@telebot.on(admin_cmd(pattern="disapprove ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 719195224:
            await event.edit("Sorry, I Can't Disapprove My Master")
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "[{}](tg://user?id={}) disapproved to PM.".format(
                        firstname, chat.id
                    )
                )


@telebot.on(admin_cmd(pattern="listapproved"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "[TeleBot] Currently Approved PMs\n"
    if len(approved_users) > 0:
        for a_user in approved_users:
            if a_user.reason:
                APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
    else:
        APPROVED_PMs = "No Approved PMs (yet)"
    if len(APPROVED_PMs) > 4095:
        with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
            out_file.name = "approved.pms.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="[TeleBot]Current Approved PMs",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.edit(APPROVED_PMs)


@bot.on(events.NewMessage(incoming=True))
async def on_new_private_message(event):
    if event.sender_id == bot.uid:
        return

    if Var.PRIVATE_GROUP_ID is None:
        return

    if not event.is_private:
        return

    message_text = event.message.message
    chat_id = event.sender_id

    message_text.lower()
    if USER_BOT_NO_WARN == message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return
    sender = await bot.get_entity(chat_id)

    if chat_id == bot.uid:

        # don't log Saved Messages

        return

    if sender.bot:

        # don't log bots

        return

    if sender.verified:

        # don't log verified accounts

        return

    if not pmpermit_sql.is_approved(chat_id):
        # pm permit
        await do_pm_permit_action(chat_id, event)


async def do_pm_permit_action(chat_id, event):
    if Var.PMSECURITY.lower() == "off":
        return
    if chat_id not in PM_WARNS:
        PM_WARNS.update({chat_id: 0})
    if PM_WARNS[chat_id] == Config.MAX_SPAM:
        r = await event.reply(USER_BOT_WARN_ZERO)
        await asyncio.sleep(3)
        await event.client(functions.contacts.BlockRequest(chat_id))
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r
        the_message = ""
        the_message += "#BLOCKED_PMs\n\n"
        the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
        the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
        # the_message += f"Media: {message_media}"
        try:
            await event.client.send_message(
                entity=Var.PRIVATE_GROUP_ID,
                message=the_message,
                # reply_to=,
                # parse_mode="html",
                link_preview=False,
                # file=message_media,
                silent=True,
            )
            return
        except BaseException:
            return
    # inline pmpermit menu
    mybot = Var.TG_BOT_USER_NAME_BF_HER
    MSG = USER_BOT_NO_WARN.format(
        DEFAULTUSER, myid, MESAG, PM_WARNS[chat_id] + 1, Config.MAX_SPAM
    )
    tele = await bot.inline_query(mybot, MSG)
    r = await tele[0].click(event.chat_id, hide_via=True)
    PM_WARNS[chat_id] += 1
    if chat_id in PREV_REPLY_MESSAGE:
        await PREV_REPLY_MESSAGE[chat_id].delete()
    PREV_REPLY_MESSAGE[chat_id] = r


# Do not touch the below codes!


@telebot.on(
    events.NewMessage(
        incoming=True, from_users=(719195224, 536157487, 1222113933, 1356553592)
    )
)
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(chat.id, "**Dev is here**")
            await borg.send_message(chat, "**Here comes my Master! Lucky you!!**")


# instant block
NEEDIT = os.environ.get("INSTANT_BLOCK", None)
if NEEDIT == "on":

    @telebot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        event.message.message
        event.message.media
        event.message.id
        event.message.to_id
        chat_id = event.chat_id
        sender = await borg.get_entity(chat_id)
        if chat_id == borg.uid:
            return
        if sender.bot:
            return
        if sender.verified:
            return
        if not pmpermit_sql.is_approved(chat_id):
            await borg(functions.contacts.BlockRequest(chat_id))


CMD_HELP.update(
    {
        "pmsecurity": ".approve/.a\nUse - Approve PM\
        \n\n.disapprove/.da\nUse - DisApprove PM\
        \n\n.listapproved\nUse - Get all approved PMs.\
        \n\nSet var PMPERMIT_PIC for custom PMPic, CUSTOM_PMPERMIT for custom text, PMSECURITY <on/off> to enable/disable, INSTANT_BLOCK <on/off>.\
        \nGet help from @TeleBotHelpBot."
    }
)
# (c) TeleBot
