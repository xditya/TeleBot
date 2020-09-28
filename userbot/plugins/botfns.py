#  (c)2020 TeleBot
#
# You may not use this plugin without proper authorship and consent from @TeleBotSupport
#
import asyncio, datetime, asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAlreadyParticipantError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import CMD_HELP
from userbot.utils import admin_cmd, sudo_cmd

@telebot.on(admin_cmd(pattern="purl ?(.*)"))
@telebot.on(sudo_cmd(pattern="purl ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.reply("**Reply to any document.**")
       return
    reply_message = await event.get_reply_message() 
    chat = "@FiletolinkTGbot"
    sender = reply_message.sender
    await event.edit("**Making public url...**")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1011636686))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await a.edit("```Please unblock me (@FiletolinkTGbot) u Nigga```")
              return
          await event.delete()
          await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)

@telebot.on(admin_cmd(pattern="reader ?(.*)"))
@telebot.on(sudo_cmd(pattern="reader ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("**Reply to a URL.**")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("**Reply to a url message.**")
       return
    chat = "@chotamreaderbot"
    sender = reply_message.sender
    await event.edit("**Making instant view...**")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=272572121))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await a.edit("```Please unblock me (@chotamreaderbot) u Nigga```")
              return
          await event.delete()
          await event.client.send_message(event.chat_id, response.message, reply_to=reply_message)
        
@telebot.on(admin_cmd(pattern="aud ?(.*)"))        
@telebot.on(sudo_cmd(pattern="aud ?(.*)")) 
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```reply to media message```")
       return
    chat = "@audiotubebot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    a = await event.reply("```Processing```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=507379365))
              await event.client.send_message(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await a.edit("```Please unblock @AudioTubeBot and try again```")
              return
          await event.delete()
          await event.client.send_file(event.chat_id, response.message.media)


