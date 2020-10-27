# Originally from Bothub
# (c) 2020 TeleBot

import asyncio
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

# from telebot.utils import admin_cmd
from telebot import CMD_HELP, bot
from telebot.utils import admin_cmd

try:
    pass
except BaseException:
    os.system("pip install instantmusic")

os.system("rm -rf *.mp3")


def bruh(name):
    os.system("instantmusic -q -s " + name)


@telebot.on(admin_cmd(outgoing=True, pattern="spd(?: |$)(.*)"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern="spd(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await eor(event, f"```Searching for Song - ``` __{link}__")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await eor(event, "`Downloading music, this might take some time...`")
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=752979930)
            )
            await bot.send_message(chat, link)
            respond = await response
        except YouBlockedUserError:
            await event.reply(
                "```Please unblock @SpotifyMusicDownloaderBot and try again```"
            )
            return
        await event.delete()
        msg = await bot.forward_messages(event.chat_id, respond.message)
        await msg.edit(
            f"Song name - __{link}__\nUploaded by [TeleBot](https://t.me/TeleBotSupport)"
        )


@telebot.on(admin_cmd(outgoing=True, pattern="netease(?: |$)(.*)"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern="netease(?: |$)(.*)"))
async def WooMai(netase):
    if netase.fwd_from:
        return
    song = netase.pattern_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {song}"
    await netase.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await netase.edit("`Downloading... Please wait`")
        try:
            msg = await conv.send_message(link)
            response = await conv.get_response()
            respond = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await netase.reply("```Please unblock @WooMaiBot and try again```")
            return
        await netase.edit("`Sending Your Music...`")
        await asyncio.sleep(3)
        await bot.send_file(netase.chat_id, respond)
    msg = await netase.client.delete_messages(
        conv.chat_id, [msg.id, response.id, respond.id]
    )
    await msg.edit(
        f"Song name - __{link}__\nUploaded by [TeleBot](https://t.me/TeleBotSupport)"
    )
    await netase.delete()


@telebot.on(admin_cmd(outgoing=True, pattern="dzd(?: |$)(.*)"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern="dzd(?: |$)(.*)"))
async def DeezLoader(Deezlod):
    if Deezlod.fwd_from:
        return
    d_link = Deezlod.pattern_match.group(1)
    if ".com" not in d_link:
        await Deezlod.edit("` I need a link to download something pro.`**(._.)**")
    else:
        await Deezlod.edit("**Initiating Download!**")
    chat = "@DeezLoadBot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            song = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await Deezlod.edit("**Error:** `unblock` @DeezLoadBot `and retry!`")
            return
        await bot.send_file(Deezlod.chat_id, song, caption=details.text)
        msg = await Deezlod.client.delete_messages(
            conv.chat_id, [msg_start.id, response.id, r.id, msg.id, details.id, song.id]
        )
        await msg.edit(
            f"Song name - __{d_link}__\nUploaded by [TeleBot](https://t.me/TeleBotSupport)"
        )
        await Deezlod.delete()


CMD_HELP.update(
    {
        "music": ".spd`<Artist - Song Title>\
            \nUsage:For searching songs from Spotify.\
            \n\n`.netease` <Artist - Song Title>\
            \nUsage:Download music with @WooMaiBot\
            \n\n`.dzd` <Spotify/Deezer Link>\
            \nUsage:Download music from Spotify or Deezer.\
            \n\n`.deezload` <spotify/deezer link> <Format>\
            \nUsage: Download music from deezer.\
            \n\n Well deezer is not available in India so create an deezer account using vpn. Set DEEZER_ARL_TOKEN in vars to make this work.\
            \n\n *Format= `FLAC`, `MP3_320`, `MP3_256`, `MP3_128`.\
            \n\n\n Guide:Video guide of arl token: [here](https://www.youtube.com/watch?v=O6PRT47_yds&feature=youtu.be) or Read [This](https://notabug.org/RemixDevs/DeezloaderRemix/wiki/Login+via+userToken)."
    }
)
