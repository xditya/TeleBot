#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

from telebot.plugins.mybot.sql.blacklist_sql import add_user_to_bl, check_is_black_list, rem_user_from_bl
from telebot.plugins.mybot.sql.users_sql import get_user_id
from telebot.plugins import OWNER_ID, TELE_NAME
from telebot import telebotConfig
from telethon import events

@tgbot.on(events.newMessage(pattern="^/ban"))
async def _(event):
    if event.sender_id == OWNER_ID:
        msg = await event.get_reply_message()
        if msg is None:
            await event.reply("Reply to a user's message to ban him!")
        user_id, reply_message_id = get_user_id(msg.id)
    else:
        return
    if check_is_black_list(user_id):
        await event.reply("You can't ban a banned user lol")
    elif not check_is_black_list(user_id):
        add_user_to_bl(user_id)
        await event.reply(f"Blocked [user]({tg://user?id={event.sender_id})")
        await tgbot.send_message(user_id, f"Why are you still here? You've been **banned** by {TELE_NAME}.")
        await tgbot.send_message(Var.PRIVATE_GROUP_ID, f"#Banned_User\nUser - {user_id}\nLink - [here](tg://user?id={user_id})")

@tgbot.on(events.NewMessage(patten="^/unblock"))
async def _(event):
    if event.sender_id == OWNER_ID:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = get_user_id(msg.id)
    else:
        return
    if not check_is_black_list(user_id):
        await event.reply("This user hasn't been banned to unban.")
    elif check_is_black_list(user_id):
        rem_user_from_bl(user_id)
        await event.reply(f"UnBanned [user](tg://user?id={user_id})")
        await tgbot.send_message(user_id, "You've been unbanned.")
        await tgbot.send_message(Var.PRIVATE_GROUP_ID, f"#UnBanned_User\nUser - {user_id}\nLink - [here](tg://user?id={user_id})")