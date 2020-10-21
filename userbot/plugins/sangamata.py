import asyncio
import logging

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot.utils import admin_cmd

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


@telebot.on(admin_cmd(pattern=("sg ?(.*)")))
@telebot.on(sudo_cmd(pattern=("sg ?(.*)", allow_sudo=True)))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await eor(event, "```reply to text message```")
        return
    chat = "@SangMataInfo_bot"
    reply_message.sender
    if reply_message.sender.bot:
        await eor(event, "```Reply to actual users message.```")
        return
    await eor(event, "```Processing```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461843263)
            )
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @sangmatainfo_bot and try again```")
            return
        if response.text.startswith("Forward"):
            await eor(event, 
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await eor(event, f"{response.message.message}")


@telebot.on(admin_cmd(pattern=("fakemail ?(.*)")))
@telebot.on(sudo_cmd(pattern=("fakemail ?(.*)", allow_sudo=True)))
async def _(event):
    if event.fwd_from:
        return
    chat = "@fakemailbot"
    await eor(event, "```Fakemail Creating, wait```")
    async with borg.conversation(chat) as conv:
        try:
            await event.client.send_message("@fakemailbot", "/generate")
            await asyncio.sleep(5)
            k = await event.client.get_messages(
                entity="@fakemailbot", limit=1, reverse=False
            )
            mail = k[0].text
            # print(k[0].text)
        except YouBlockedUserError:
            await event.reply("```Please unblock @fakemailbot and try again```")
            return
        await eor(event, mail)


@telebot.on(admin_cmd(pattern=("mailid ?(.*)")))
@telebot.on(sudo_cmd(pattern=("mailid ?(.*)", allow_sudo=True)))
async def _(event):
    if event.fwd_from:
        return
    chat = "@fakemailbot"
    await eor(event, "```Fakemail list getting```")
    async with borg.conversation(chat) as conv:
        try:
            await event.client.send_message("@fakemailbot", "/id")
            await asyncio.sleep(5)
            k = await event.client.get_messages(
                entity="@fakemailbot", limit=1, reverse=False
            )
            mail = k[0].text
            # print(k[0].text)
        except YouBlockedUserError:
            await event.reply("```Please unblock @fakemailbot and try again```")
            return
        await eor(event, mail)


@telebot.on(admin_cmd(pattern=("ub ?(.*)")))
@telebot.on(sudo_cmd(pattern=("ub ?(.*)", allow_sudo=True)))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await eor(event, "```reply to text message```")
        return
    chat = "@uploadbot"
    reply_message.sender
    if reply_message.sender.bot:
        await eor(event, "```Reply to actual users message.```")
        return
    await eor(event, "```Processing```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=97342984)
            )
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @uploadbot and try again```")
            return
        if response.text.startswith("Hi!,"):
            await eor(event, 
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await eor(event, f"{response.message.message}")


@telebot.on(admin_cmd(pattern=("gid ?(.*)")))
@telebot.on(sudo_cmd(pattern=("gid ?(.*)", allow_sudo=True)))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await eor(event, "```reply to text message```")
        return
    chat = "@getidsbot"
    reply_message.sender
    if reply_message.sender.bot:
        await eor(event, "```Reply to actual users message.```")
        return
    await eor(event, "```Processing```")
    async with borg.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=186675376)
            )
            await borg.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```you blocked bot```")
            return
        if response.text.startswith("Hello,"):
            await eor(event, 
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await eor(event, f"{response.message.message}")
