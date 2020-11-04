import asyncio

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI
from telethon import events

from telebot import CMD_HELP
from telebot.utils import admin_cmd

# Non-SQL Mode
ACC_LYDIA = {}

if Var.LYDIA_API_KEY:
    api_key = Var.LYDIA_API_KEY
    api_client = API(api_key)
    lydia = LydiaAI(api_client)


@telebot.on(admin_cmd(pattern="repcf", outgoing=True))
@telebot.on(sudo_cmd(pattern="repcf", allow_sudo=True))
async def repcf(event):
    if event.fwd_from:
        return
    await eor(event, "Processing...")
    try:
        session = lydia.create_session()
        session.id
        reply = await event.get_reply_message()
        msg = reply.text
        text_rep = session.think_thought(msg)
        await eor(event, "**sun bsdk**: {0}".format(text_rep))
    except Exception as e:
        await eor(event, str(e))


@telebot.on(admin_cmd(pattern="addcf", outgoing=True))
@telebot.on(sudo_cmd(pattern="addcf", allow_sudo=True))
async def addcf(event):
    if event.fwd_from:
        return
    await eor(event, "Running on Non-SQL mode for now...")
    await asyncio.sleep(3)
    await eor(event, "Processing...")
    reply_msg = await event.get_reply_message()
    if reply_msg:
        session = lydia.create_session()
        session.id
        if reply_msg.from_id is None:
            return await eor(event, "Invalid user type.")
        ACC_LYDIA.update({(event.chat_id & reply_msg.from_id): session})
        await eor(
            event,
            "Lydia successfully (re)enabled for user: {} in chat: {}".format(
                str(reply_msg.from_id), str(event.chat_id)
            ),
        )
    else:
        await eor(event, "Reply to a user to activate Lydia AI on them")


@telebot.on(admin_cmd(pattern="remcf", outgoing=True))
@telebot.on(sudo_cmd(pattern="remcf", allow_sudo=True))
async def remcf(event):
    if event.fwd_from:
        return
    await eor(event, "Running on Non-SQL mode for now...")
    await asyncio.sleep(3)
    await eor(event, "Processing...")
    reply_msg = await event.get_reply_message()
    try:
        del ACC_LYDIA[event.chat_id & reply_msg.from_id]
        await eor(
            event,
            "Lydia successfully disabled for user: {} in chat: {}".format(
                str(reply_msg.from_id), str(event.chat_id)
            ),
        )
    except Exception:
        await eor(event, "This person does not have Lydia activated on him/her.")


@bot.on(events.NewMessage(incoming=True))
async def user(event):
    event.text
    try:
        session = ACC_LYDIA[event.chat_id & event.sender_id]
        msg = event.text
        async with event.client.action(event.chat_id, "typing"):
            text_rep = session.think_thought(msg)
            wait_time = 0
            for i in range(len(text_rep)):
                wait_time = wait_time + 0.1
            await asyncio.sleep(wait_time)
            await event.reply(text_rep)
    except (KeyError, TypeError):
        return


CMD_HELP.update(
    {
        "lydia": ".repcf <reply to user>\nUse - Reply to that message with AI.\
        \n\n.addcf <reply to user>\nUse - Activate AI on the user.\
        \n\n.remcf <reply to user>\nUse - DeActivate AI on the user."
    }
)
