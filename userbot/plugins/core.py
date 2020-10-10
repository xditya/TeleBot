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

from userbot.utils import command, remove_plugin, load_module, admin_cmd
from pathlib import Path
import asyncio
import os
import userbot.utils
from datetime import datetime
from userbot.utils import admin_cmd, sudo_cmd
from telethon.tl.types import InputMessagesFilterDocument

DELETE_TIMEOUT = 5
thumb_image_path = "./TeleBot.png"

@telebot.on(admin_cmd(pattern="install"))
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

@telebot.on(admin_cmd(pattern="unload (?P<shortname>\w+)$"))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"TeleBot has successfully unloaded {shortname}")
    except Exception as e:
        await event.edit("TeleBot has successfully unloaded {shortname}\n{}".format(shortname, str(e)))

@telebot.on(admin_cmd(pattern="load (?P<shortname>\w+)$"))
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

@telebot.on(admin_cmd(pattern=r"installall$"))
async def install(event):
	if event.fwd_from:
		return
	documentss = await event.client.get_messages(event.chat_id, None ,search='.py', filter=InputMessagesFilterDocument)
	total = int(documentss.total)
	total_doxx = range(0, total)
	b = await event.client.send_message(event.chat_id, f"**Installing {total} plugins...**\n`This msg will be deleted after the installation gets completed`")
	text =  "**Installing Plugins...**\n\n"
	a = await event.client.send_message(event.chat_id, text)
	if total == 0:
		await a.edit("**No plugins to install.**")
		await event.delete()
		return
	for ixo in total_doxx:
		mxo = documentss[ixo].id
		downloaded_file_name = await event.client.download_media(await event.client.get_messages(event.chat_id, ids=mxo), "userbot/plugins/")
		if "(" not in downloaded_file_name:
			path1 = Path(downloaded_file_name)
			shortname = path1.stem
			try:
				load_module(shortname.replace(".py", ""))
				text += f"**• Installed** `{(os.path.basename(downloaded_file_name))}` **successfully.**\n"
			except:
				text += f"**• Error installing** `{(os.path.basename(downloaded_file_name))}`\n"
		else:
			text += f"**• Plugin** `{(os.path.basename(downloaded_file_name))}` **already installed.**\n"
		await a.edit(f"{text}\n**Installed every plugin.**")
		await event.delete()
		await b.delete()
