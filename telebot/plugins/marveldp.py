# Made By @MarioDevs Keep Credits If You Are Goanna Kang This Lol

# And Thanks To The Creator Of Autopic This Script Was Made from Snippets
# From That Script

# Usage .marveldp I'm Not Responsible For Any Ban caused By This

# Marvel dp's by @tansique_17

import asyncio
import os
import random
import re
import urllib

import requests
from telethon.tl import functions

from telebot import CMD_HELP
from telebot.utils import admin_cmd

COLLECTION_STRING = [
    "avengers-logo-wallpaper",
    "avengers-hd-wallpapers-1080p",
    "avengers-iphone-wallpaper",
    "iron-man-wallpaper-1920x1080",
    "iron-man-wallpapers",
    "Marvel-Shield-iPhone-Wallpaper",
    "Shield-Logo-Wallpaper",
    "Marvel-Shield-Logo-Wallpaper",
    "Agents-of-Shield-Wallpaper",
    "Agents-of-Shield-iPhone-Wallpaper",
    "Agents-of-Shield-Wallpapers-HD" "Thor-Wallpaper-1920x1080",
    "Thor-Wallpapers",
    "Avengers-HD-Wallpapers-1080p",
    "Avengers-Wallpaper-for-Desktop",
    "Avengers-4K-Wallpaper",
    "Avengers-Age-of-Ultron-Wallpaper",
    "Avengers-Civil-War-Wallpaper",
    "Avengers-2-Wallpapers",
    "Avengers-Logo-Wallpaper",
    "Marvel-Avengers-Desktop-Wallpaper",
    "4K-Deadpool-Wallpaper",
    "3D-Deadpool-Logo-Wallpaper",
    "Deadpool-HD-Desktop-Wallpaper",
    "Cool-Deadpool-Wallpaper",
    "Thor-Wallpaper-HD",
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


@telebot.on(admin_cmd(pattern="marveldp ?(.*)"))
async def main(event):

    await event.edit(
        "**Starting Marvel Profile Pic's...\n\nDone !!! Check Your DP . Plugin made By @Tansique_17. Thank you @Mariodevs for inspiration.**"
    )

    while True:

        await animepp()

        file = await event.client.upload_file("donottouch.jpg")

        await event.client(functions.photos.UploadProfilePhotoRequest(file))

        os.system("rm -rf donottouch.jpg")

        await asyncio.sleep(600)  # Edit this to your required needs


CMD_HELP.update({"marveldp": ".marveldp\nUse - Auto Changing marvel dp."})
