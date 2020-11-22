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

#   thanks to @RaphielGang for the base.

"""
Get detailed info about any user
"""

import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from telebot import CMD_HELP

TMP_DOWNLOAD_DIRECTORY = "./"


@telebot.on(admin_cmd(pattern="whois(?: |$)(.*)"))
async def who(event):
    """ For .whois command, get info about a user. """
    if event.fwd_from:
        return

    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)
    caption = await fetch_info(replied_user, event)
    message_id_to_reply = event.message.reply_to_msg_id
    replied_user_profile_photos = await borg(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )

    if not message_id_to_reply:
        message_id_to_reply = None

    await borg.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
    )
    await event.delete()


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit("**ERROR**\n" + str(err))
            return None
        replied_user_profile_photos = await borg(
            GetUserPhotosRequest(
                user_id=replied_user.user.id, offset=42, max_id=0, limit=80
            )
        )

    return replied_user


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    first_name = first_name.replace("\u2060", "") if first_name else (" ")
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    username = "@{}".format(username) if username else ("This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio

    if user_id != (await event.client.get_me()).id:
        common_chat = replied_user.common_chats_count
    else:
        common_chat = "I've seen them in... Wow. Are they stalking me? "
        common_chat += "They're in all the same places I am... oh. It's me."

    caption = "<u><b>Dᴇᴛᴀɪʟᴇᴅ UsᴇʀIɴғᴏ</b></u>\n\n"
    caption += f"✯ <b>Fɪʀsᴛ Nᴀᴍᴇ</b>: <code>{first_name}</code> \n"
    caption += f"✯ <b>Lᴀsᴛ Nᴀᴍᴇ</b>: <code>{last_name}</code> \n"
    caption += f"✯ <b>UsᴇʀNᴀᴍᴇ</b>: <code>{username}</code> \n"
    caption += f"✯ <b>Is Bᴏᴛ</b>: <code>{is_bot}</code> \n"
    caption += f"✯ <b>Is Rᴇsᴛʀɪᴄᴛᴇᴅ</b>: <code>{restricted}</code> \n"
    caption += f"✯ <b>Is Vᴇʀɪғɪᴇᴅ ʙʏ Tᴇʟᴇɢʀᴀᴍ</b>: <code>{verified}</code> \n"
    caption += f"✯ <b>ID</b>: <code>{user_id}</code> \n"
    caption += f"✯ <b>Bɪᴏ</b>: <code>{user_bio}</code> \n\n"
    caption += f"✯ <b>Nᴜᴍʙᴇʀ ᴏғ Pʀᴏғɪʟᴇ Pɪᴄs</b>: <code>{replied_user_profile_photos_count}</code> \n"
    caption += f"\n✯ <b>Cᴏᴍᴍᴏɴ Cʜᴀᴛs</b>: <code>{common_chat} </code>\n\n"
    caption += f"✯ <b>Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ</b>: "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'

    return caption


CMD_HELP.update(
    {
        "whois": ".whois <id/reply to mssg>\nUse - Get full details about a persons telegram account."
    }
)
