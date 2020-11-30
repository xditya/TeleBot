# Made For DARK COBRA and TELEBOT...
# Made by team cobra with @xditya
# Retrieves the name history and the username history of the replied user..

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern="sg ?(.*)"))
@telebot.on(sudo_cmd(pattern="sg ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ok = await eor(event, "Checking...")
    if not event.reply_to_msg_id:
        await ok.edit("Reply to any user message.")
        return
    reply_message = await event.get_reply_message()
    chat = "Sangmatainfo_bot"
    sender = reply_message.sender.id
    if reply_message.sender.bot:
        await ok.edit("Reply to actual users message and not a bots...")
        return
    async with event.client.conversation(chat) as conv:
        try:
            response1 = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461843263)
            )
            response2 = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461843263)
            )
            response3 = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461843263)
            )
            await conv.send_message("/search_id {}".format(sender))
            response1 = await response1
            response2 = await response2
            response3 = await response3
        except YouBlockedUserError:
            await ok.edit("Please unblock ( @Sangmatainfo_bot ) ")
            return
        if response1.text.startswith("No records found"):
            await event.edit("User never changed his Username...")
        else:
            await event.delete()
            await telebot.send_message(event.chat_id, response2.message)

            await telebot.send_message(event.chat_id, response3.message)


CMD_HELP.update(
    {
        "sangmata": ".sg <reply to user>\nUse - Get full name and username history of the person."
    }
)
