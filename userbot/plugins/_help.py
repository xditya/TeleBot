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
import requests
from telethon import functions
from userbot import ALIVE_NAME, CMD_HELP, CMD_LIST
from userbot.helpers.utils import yaml_format

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot User"

@telebot.on(admin_cmd(outgoing=True, pattern="help ?(.*)"))
async def cmd_list(event):
    reply_to_id = None
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = ("{count} commands in {plugincount} plugins\n\n")
        count = 0
        plugincount = 0
        for i in sorted(CMD_LIST):
            plugincount += 1
            string += f"**{plugincount}) Commands found in **" + i + " - \n"
            for iter_list in CMD_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                count += 1   
            string += "\n\n© @TeleBotSupport" 
        if len(string) > 4095:
            with io.BytesIO(str.encode(string)) as out_file:
                out_file.name = "cmd.txt"
                await tgbot.send_file(
                    event.sender_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="**Commands found in the plugin.**",
                    reply_to=reply_to_id,
                    )
                await event.delete()
        else:
            await event.edit(string.format(count=count, plugincount=plugincount))
        return
    if input_str:
        if input_str in CMD_LIST:
            string = "<b>{count} Commands found in plugin {input_str}:</b>\n\n"
            count = 0
            for i in CMD_LIST[input_str]:
                string += f" <code>{i}</code>"
                string += "\n"
                count += 1
            string += "\n\n <bold>© @TeleBotSupport</bold>" 
            await event.edit(
                string.format(count=count, input_str=input_str), parse_mode="HTML"
            )
        else:
            await event.edit(input_str + " is not a valid plugin!")
            await asyncio.sleep(3)
            await event.delete()
    else:
        help_string = "TeleBot Help Menu"
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        results = await bot.inline_query(  # pylint:disable=E0602
            tgbotusername, help_string
        )
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()
