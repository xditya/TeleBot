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

from googletrans import Translator

from telebot import CMD_HELP

translator = Translator()


@telebot.on(admin_cmd(pattern="langdet ?(.*)"))
async def tele(event):
    theword = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        theword = previous_message.message
    ok = translator.detect("theword")
    await event.edit(
        f"**The given sentence/word** - `{theword}`\n\n**Detected language** - `{ok.lang}`\n\n**Detection Accuracy** - `{ok.confidence}`"
    )


CMD_HELP.update(
    {
        "langdetect": ".langdet <sentence/reply to sentence>\nUse - Find in which language the given message is."
    }
)
