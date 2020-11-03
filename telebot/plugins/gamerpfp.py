# Made By @TeleBotComms Keep Credits If You Are Goanna Kang This Lol

# And Thanks To The Creator Of Autopic This Script Was Made from Snippets
# From That Script

# Usage .gamerpfp  Im Not Responsible For Any Ban caused By This

import asyncio
import os
import random
import re
import urllib

import requests
from telethon.tl import functions
from uniborg.util import admin_cmd

from telebot import CMD_HELP

COLLECTION_STRING = [
    "star-wars-wallpaper-1080p",
    "4k-sci-fi-wallpaper",
    "star-wars-iphone-6-wallpaper",
    "kylo-ren-wallpaper",
    "darth-vader-wallpaper",
]


async def animepp():

    os.system("rm -rf donot.jpg")

    rnd = random.randint(0, len(COLLECTION_STRING) - 1)

    pack = COLLECTION_STRING[rnd]

    pc = requests.get("http://getwallpapers.com/collection/" + pack).text

    f = re.compile(r"/\w+/full.+.jpg")

    f = f.findall(pc)

    fy = "http://getwallpapers.com" + random.choice(f)

    print(fy)

    if not os.path.exists("f.ttf"):

        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf",
            "f.ttf",
        )

    urllib.request.urlretrieve(fy, "donottouch.jpg")


@telebot.on(admin_cmd(pattern="gamerpfp ?(.*)"))
async def main(event):

    # Owner @NihiNivi
    await event.edit(
        "**Starting Gamer Profile Pic.\n\nModded by[TeleBot](https://github.com/xditya/TeleBot)"
    )

    while True:

        await animepp()

        file = await event.client.upload_file("donottouch.jpg")

        await event.client(functions.photos.UploadProfilePhotoRequest(file))

        os.system("rm -rf donottouch.jpg")

        await asyncio.sleep(3600)  # Edit this to your required needs


CMD_HELP.update({"gamerpfp": ".gamerpfp\nUse - Autochanging gamer profile pic."})
