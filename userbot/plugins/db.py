# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# thanks to penn5 for bug fixing
"""cmd is `.DBS` Shows database related info."""

import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from uniborg.util import admin_cmd
import userbot
from os import remove
from platform import python_version, uname
from shutil import which
from telethon import version
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from shutil import which
from os import remove
from telethon import version
from platform import python_version, uname
from telethon import version
from sample_config import Config
from sample_config import is_mongo_alive, is_redis_alive

# ================= CONSTANT =================
DEFAULTUSER = Config.ALIVE_NAME if Config.ALIVE_NAME else uname().node
# ============================================



@borg.on(admin_cmd("DBS"))
async def amireallyDBS(DBS):
    if not is_mongo_alive() and not is_redis_alive():
        db = "Both Mongo and Redis Database seems to be failing!"
    elif not is_mongo_alive():
        db = "Mongo DB seems to be failing!"
    elif not is_redis_alive():
        db = "Redis Cache seems to be failing!"
    else:
        db = "Databases functioning normally!"
    await DBS.edit("`"
                     f"User: {DEFAULTUSER} \n"
                     f"Database status: {db}\n"
                     f"TeleBot Version: v2.13.02"
                     "`")
