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

from telegraph import Telegraph
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from telebot import CMD_HELP
from telebot.telebotConfig import Var
from telebot.utils import admin_cmd, sudo_cmd

telegraph = Telegraph()
mee = telegraph.create_account(short_name="telebot")


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
    reply_message.sender
    await eor(event, "**Making public url...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1011636686)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await eor(event, "```Please unblock me (@FiletolinkTGbot) u Nigga```")
            return
        await event.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_message
        )


@telebot.on(admin_cmd(pattern="reader ?(.*)"))
@telebot.on(sudo_cmd(pattern="reader ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "**Reply to a URL.**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await eor(event, "**Reply to a url message.**")
        return
    chat = "@chotamreaderbot"
    reply_message.sender
    await eor(event, "**Making instant view...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=272572121)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await eor(event, "```Please unblock me (@chotamreaderbot) u Nigga```")
            return
        await event.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_message
        )


@telebot.on(admin_cmd(pattern="aud ?(.*)"))
@telebot.on(sudo_cmd(pattern="aud ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eor(event, "```reply to media message```")
        return
    chat = "@audiotubebot"
    reply_message.sender
    if reply_message.sender.bot:
        await eor(event, "```Reply to actual users message.```")
        return
    await event.reply("```Processing```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=507379365)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await eor(event, "```Please unblock @AudioTubeBot and try again```")
            return
        await event.delete()
        await event.client.send_file(event.chat_id, response.message.media)


@telebot.on(admin_cmd(pattern="instadl ?(.*)"))
@telebot.on(sudo_cmd(pattern="instadl ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("**Reply to a instagram url.**")
        return
    reply_message = await event.get_reply_message()
    chat = "@instadownloadingbot"
    reply_message.sender
    await eor(event, "**Downloading the post...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1310260390)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await eor(event, "```Please unblock me (@instadownloadingbot) u Nigga```")
            return
        await event.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_message
        )


@telebot.on(admin_cmd(pattern="stats$"))
@telebot.on(sudo_cmd(pattern="stats$", allow_sudo=True))
async def stats(event):
    if event.fwd_from:
        return
    botusername = Var.TG_BOT_USER_NAME_BF_HER
    noob = "stats"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="xogame$"))
@telebot.on(sudo_cmd(pattern="xogame$", allow_sudo=True))
async def gamez(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="whisper ?(.*)"))
@telebot.on(sudo_cmd(pattern="whisper ?(.*)", allow_sudo=True))
async def wspr(event):
    if event.fwd_from:
        return
    wwwspr = event.pattern_match.group(1)
    botusername = "@whisperBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, wwwspr)
    await tap[0].click(event.chat_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="crack ?(.*)"))
@telebot.on(sudo_cmd(pattern="crack ?(.*)", allow_sudo=True))
async def mod(event):
    if event.fwd_from:
        return
    modr = event.pattern_match.group(1)
    botusername = "@PremiumAppBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, modr)
    await tap[0].click(event.chat_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="checkspam ?(.*)"))
@telebot.on(sudo_cmd(pattern="checkspam ?(.*), allow_sudo=True"))
async def _(event):
    bot = "@SpamBot"
    if event.fwd_from:
        return
    sysarg = event.pattern_match.group(1)
    if sysarg == "":
        async with borg.conversation(bot) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/start")
                audio = await conv.get_response()
                final = ("See if you are limited..\n(c)@TeleBotSupport", "")
                await borg.send_message(event.chat_id, audio.text)
                await event.delete()
            except YouBlockedUserError:
                await eor(event, "**Error:** `unblock` @spambot `and retry!")


@telebot.on(admin_cmd(pattern="gitdl ?(.*)"))
@telebot.on(sudo_cmd(pattern="gitdl ?(.*), allow_sudo=True"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("**Reply to a github repo url.**")
        return
    reply_message = await event.get_reply_message()
    chat = "@gitdownloadbot"
    reply_message.sender
    await eor(event, "**Downloading the repository...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1282593576)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await eor(event, "```Please unblock me (@gitdownloadbot) u Nigga```")
            return
        await event.delete()
        x = await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_message
        )
        await x.edit(
            "Downloaded by [TeleBot](t.me/TeleBotSupport), via @gitdownloadbot"
        )


@telebot.on(admin_cmd(pattern="imusic ?(.*)"))
@telebot.on(sudo_cmd(pattern="imusic ?(.*)", allow_sudo=True))
async def tel(event):
    if event.fwd_from:
        return
    botusername = "@vkmusic_bot"
    tele = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, tele)
    await tap[0].click(event.chat_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="font ?(.*)"))
@telebot.on(sudo_cmd(pattern="font ?(.*)", allow_sudo=True))
async def _(event):
    bot = "@fontsgenbot"
    if event.fwd_from:
        return
    sysarg = event.pattern_match.group(1)
    if sysarg == "":
        await event.edit("Give me a text to sylize pero")
    else:
        async with borg.conversation(bot) as conv:
            try:
                x = await eor(event, "`Making the text stylish..`")
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message(sysarg)
                audio = await conv.get_response()
                title = "Stylish Fonts"
                topaste = audio.text
                topaste = topaste.replace("\n", "<br>")
                response = telegraph.create_page(title, html_content=topaste)
                link = response["path"]
                await x.edit(
                    f"**Normal Text** - {sysarg}\n**Stylised text** - [here](https://telegra.ph/{link})",
                    link_preview=False,
                )
            except YouBlockedUserError:
                await x.edit("**Error:** `unblock` @fontsgenbot `and retry!")


CMD_HELP.update(
    {
        "botfns": ".purl <reply to file>\nUse - Get a direct download link of that file/doc/pic/vid\
        \n\n.reader <reply to url>\nUse - Get an instant view of that site.\
        \n\n.aud <reply to youtube link>\nUse - Get audo from that youtube video\
        \n\n.instadl <reply to instagram url>\\nUse - Download that instagram post.\
        \n\n.stats\nUse - To see the stats of your bot.\
        \n\n.xogame\nUse - Start an XO-Game\
        \n\n.whisper <message> <target username/id>\nUse - Send a whisper message to that person.\
        \n\n.crack <app name>\nUse - Get the crack/mod of an app.\
        \n\n.checkspam\nUse - Check if you are limited.\
        \n\n.gitdl <reply to github link>\nUse - Download the main branch of that git repo.\
        \n\n.imusic <song name>\nUse - Get the song.\
        \n\n.font <text>\nUse - Generate some stylish fonts."
    }
)
