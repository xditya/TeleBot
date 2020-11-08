# Adapted from OpenUserBot for Uniborg

"""Download & Upload Images on Telegram\n
Syntax: `.img <Name>` or `.img (replied message)`
\n Upgraded and Google Image Error Fixed by @NeoMatrix90 aka @kirito6969
"""

import os
import shutil
from re import findall

from uniborg.util import admin_cmd

from telebot import CMD_HELP
from telebot.google_images_download import googleimagesdownload


@telebot.on(admin_cmd(pattern="img ?(.*)"))
@telebot.on(sudo_cmd(pattern="img ?(.*)", allow_sudo=True))
async def img_sampler(event):
    await eor(event, "`Processing ...`")
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        query = reply.message
    else:
        await eor(event, "`What I am Supposed to Search u Dumb Ass(Donkey)`")
        return

    lim = findall(r"lim=\d+", query)
    # lim = event.pattern_match.group(1)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 5
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


CMD_HELP.update({"img": ".img <query>\nUse - Get images matching the query."})
