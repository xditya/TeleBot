# Code from pro sar Spechide's fork of Uniborg.
"""Rename Telegram Files
Syntax:
.rename new.file.name"""

import os
import time
from datetime import datetime

from uniborg.util import admin_cmd

from telebot import CMD_HELP
from telebot.telebotConfig import Config

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@telebot.on(admin_cmd(pattern="rename (.*)"))
@telebot.on(sudo_cmd(pattern="rename (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    xyz = Config.CMD_HNDLR
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    await eor(event, "**Downloading, renaming and uploading...**")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        end = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
        )
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            time.time()
            await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await eor(
                event,
                "Downloaded in {} seconds 😎. Uploaded in {} seconds 🥳.".format(
                    ms_one, ms_two
                ),
            )
        else:
            await eor(event, "File Not Found {}".format(input_str))
    else:
        await eor(
            event,
            f"Syntax ~ `{xyz}rename file_name.extension` as reply to a Telegram media",
        )


CMD_HELP.update(
    {"rename": ".rename <filename.extension> <reply to media>\nUse - Rename the media."}
)
