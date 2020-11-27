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

from telethon.errors.rpcerrorlist import YouBlockedUserError

from telebot import CMD_HELP

bot = "@MissRose_bot"


@telebot.on(admin_cmd(pattern="fstat ?(.*)"))
@telebot.on(sudo_cmd(pattern="fstat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ok = await event.edit("`Checking...`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        sysarg = str(previous_message.sender_id)
        user = f"[user](tg://user?id={sysarg})"
    else:
        sysarg = event.pattern_match.group(1)
        user = sysarg
    if sysarg == "":
        await ok.edit(
            "`Give me someones id, or reply to somones message to check his/her fedstat.`"
        )
        return
    else:
        async with borg.conversation(bot) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + sysarg)
                audio = await conv.get_response()
                if "Looks like" in audio.text:
                    await audio.click(0)
                    await asyncio.sleep(2)
                    audio = await conv.get_response()
                    await telebot.send_file(
                        event.chat_id,
                        audio,
                        caption=f"List of feds {user} has been banned in.\n\nCollected using TeleBot.",
                    )
                else:
                    await borg.send_message(event.chat_id, audio.text)
                await event.delete()
            except YouBlockedUserError:
                await ok.edit("**Error**\n `Unblock` @MissRose_Bot `and try again!")


@telebot.on(admin_cmd(pattern="fedinfo ?(.*)"))
@telebot.on(sudo_cmd(pattern="fedinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ok = await event.edit("`Extracting information...`")
    sysarg = event.pattern_match.group(1)
    async with borg.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + sysarg)
            audio = await conv.get_response()
            await ok.edit(audio.text + "\n\nFedInfo Excracted by TeleBot")
        except YouBlockedUserError:
            await ok.edit("**Error**\n `Unblock` @MissRose_Bot `and try again!")


CMD_HELP.update(
    {
        "fedstuff": ".fstat <username/userid/reply to user>\nUse - To check the persons fedban stat in @MissRose_Bot.\
        \n\n.fedinfo <fedid>\nUse - To see info about the fed."
    }
)
