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

import requests

from . import CMD_HELP


@telebot.on(admin_cmd(pattern="grpcnt ?(.*)"))
async def counter(tele):
    chat = tele.pattern_match.group(1)
    if not tele.is_private:
        chat = f"@{tele.chat.username}"
    if not chat:
        return await tele.edit("`Give a channel/group @username`")
    request_url = (
        "https://api.telegram.org/bot{}/getChatMembersCount?chat_id={}".format(
            Var.TG_BOT_TOKEN_BF_HER, chat
        )
    )
    current_response = requests.get(request_url).json()
    try:
        ok = current_response["result"]
    except BaseException:
        return await tele.edit("`Invalid UserName or Not a Public Group!!`")
    await tele.edit(f"`Chat` - {chat}\n`Members` - {ok}")


CMD_HELP.update(
    {
        "grps": ".grpcnt <use in group/give group @username>\
        \nUse - Get member count of that group."
    }
)
