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
"""Remove.BG Plugin for @UniBorg
Syntax: .remove.bg https://link.to/image.extension
Syntax: .remove.bg as reply to a media"""
import io
import os
from datetime import datetime

import requests

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern=r"remove\.bg ?(.*)"))
@telebot.on(sudo_cmd(pattern=r"remove\.bg ?(.*)", allow_sudo=True))
async def _(event):
    HELP_STR = "`.remove.bg` as reply to a media, or give a link as an argument to this command"
    if event.fwd_from:
        return
    if Config.REM_BG_API_KEY is None:
        await eor(
            event,
            "Get your API key from [here](https://www.remove.bg/) and add in the var `REM_BG_API_KEY` for this plugin to work.",
        )
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        await eor(event, "`Analysing...`")
        try:
            downloaded_file_name = await borg.download_media(
                reply_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await eor(event, str(e))
            return
        else:
            await eor(event, "`Sending to ReMove.BG`")
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await eor(event, "sending to ReMove.BG")
        output_file_name = ReTrieveURL(input_str)
    else:
        await eor(event, HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "TeleBot-Rmbg.png"
            await borg.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
        end = datetime.now()
        ms = (end - start).seconds
        await eor(
            event,
            "Removed dat annoying Backgroup in {} seconds, powered by @TeleBotHelp".format(
                ms
            ),
        )
    else:
        await eor(
            event,
            "RemoveBG returned an error - \n`{}`".format(
                output_file_name.content.decode("UTF-8")
            ),
        )


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )
    return r


CMD_HELP.update(
    {"removebg": ".remove.bg <reply to pic>\nUse - Remove the background of the pic."}
)
