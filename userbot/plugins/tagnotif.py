# (c) Shrimadhav U K
#
# This file is part of @UniBorg
#
# @UniBorg is free software; you cannot redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# @UniBorg is not distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Modified to suit needs, by @its_xditya
#
"""-_-
"""
from telethon import custom, events
from telethon.tl.types import Channel
from telethon.utils import get_display_name

from telebot.telebotConfig import Config

if Config.TAG_LOG:
    NEEDTOLOG = int(Config.TAG_LOG)

if Config.TAG_LOG:

    @telebot.on(
        events.NewMessage(
            incoming=True,
            blacklist_chats=Config.UB_BLACK_LIST_CHAT,
            func=lambda e: (e.mentioned),
        )
    )
    async def all_messages_catcher(event):
        # the bot might not have the required access_hash to mention the
        # appropriate PM
        await event.forward_to(Var.TG_BOT_USER_NAME_BF_HER)

        # construct message
        # the message format is stolen from @MasterTagAlertBot
        ammoca_message = ""

        who_ = await event.client.get_entity(event.sender_id)
        if who_.bot or who_.verified or who_.support:
            return

        who_m = f"[{get_display_name(who_)}](tg://user?id={who_.id})"

        where_ = await event.client.get_entity(event.chat_id)

        where_m = get_display_name(where_)
        button_text = "📃 Go to Message  "

        if isinstance(where_, Channel):
            message_link = f"https://t.me/c/{where_.id}/{event.id}"
        else:
            # not an official link,
            # only works in DrKLO/Telegram,
            # for some reason
            message_link = f"tg://openmessage?chat_id={where_.id}&message_id={event.id}"
            # Telegram is weird :\

        ammoca_message += f"{who_m} tagged you in [{where_m}]({message_link})"
        if NEEDTOLOG is not None:
            await tgbot.send_message(
                entity=NEEDTOLOG,
                message=ammoca_message,
                link_preview=False,
                buttons=[[custom.Button.url(button_text, message_link)]],
                silent=True,
            )
        else:
            return


# Tag notifier plugin, to get notifications if someone tags you.
# Set TAG_LOG if you want this plugin to work.
