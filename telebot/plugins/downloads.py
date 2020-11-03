"""
Gdrive and mega downloader plugin for TeleBot
Ported from other bots
"""
import asyncio
import errno
import json
import math
import multiprocessing
import os
import re
import time
from asyncio import create_subprocess_shell as asyncSubprocess
from asyncio.subprocess import PIPE as asyncPIPE
from urllib.error import HTTPError

import requests
from pySmartDL import SmartDL

from telebot import CMD_HELP, LOGS
from telebot.utils import admin_cmd, humanbytes, time_formatter


async def download_file_from_google_drive(id):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = await get_confirm_token(response)
    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    headers = response.headers
    content = headers["Content-Disposition"]
    destination = await get_file_name(content)

    file_name = await save_response_content(response, destination)
    return file_name


async def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


async def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return destination


async def get_id(link):  # Extract File Id from G-Drive Link
    file_id = ""
    c_append = False
    if link[1:33] == "https://drive.google.com/file/d/":
        link = link[33:]
        fid = ""
        for c in link:
            if c == "/":
                break
            fid = fid + c
        return fid
    for c in link:
        if c == "=":
            c_append = True
        if c == "&":
            break
        if c_append:
            file_id = file_id + c
    file_id = file_id[1:]
    return file_id


async def get_file_name(content):
    file_name = ""
    c_append = False
    for c in str(content):
        if c == '"':
            c_append = True
        if c == ";":
            c_append = False
        if c_append:
            file_name = file_name + c
    file_name = file_name.replace('"', "")
    print("File Name: " + str(file_name))
    return file_name


@telebot.on(admin_cmd(pattern=f"gdl", outgoing=True))
@telebot.on(sudo_cmd(pattern=f"gdl", allow_sudo=True))
async def g_download(event):
    if event.fwd_from:
        return
    drive_link = event.text[4:]
    print("Drive Link: " + drive_link)
    file_id = await get_id(drive_link)
    await eor(event, "Downloading Requested File from G-Drive...")
    file_name = await download_file_from_google_drive(file_id)
    await eor(event, "File Downloaded.\nName: `" + str(file_name) + "`")


# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


TEMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY


async def subprocess_run(megadl, cmd):
    subproc = await asyncSubprocess(cmd, stdout=asyncPIPE, stderr=asyncPIPE)
    stdout, stderr = await subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        await megadl.edit(
            "**An error was detected while running subprocess.**\n"
            f"exitCode : `{exitCode}`\n"
            f"stdout : `{stdout.decode().strip()}`\n"
            f"stderr : `{stderr.decode().strip()}`"
        )
        return exitCode
    return stdout.decode().strip(), stderr.decode().strip(), exitCode


@telebot.on(admin_cmd(outgoing=True, pattern=r"mega(?: |$)(.*)"))
async def mega_downloader(megadl):
    await megadl.edit("`Collecting information...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    msg_link = await megadl.get_reply_message()
    link = megadl.pattern_match.group(1)
    if link:
        pass
    elif msg_link:
        link = msg_link.text
    else:
        return await megadl.edit("Usage: `.mega` **<MEGA.nz link>**")
    try:
        link = re.findall(r"\bhttps?://.*mega.*\.nz\S+", link)[0]
        # - Mega changed their URL again -
        if "file" in link:
            link = link.replace("#", "!").replace("file/", "#!")
        elif "folder" in link or "#F" in link or "#N" in link:
            await megadl.edit("`folder download support are removed...`")
            return
    except IndexError:
        await megadl.edit("`MEGA.nz link not found...`")
        return None
    cmd = f"bin/megadown -q -m {link}"
    result = await subprocess_run(megadl, cmd)
    try:
        data = json.loads(result[0])
    except json.JSONDecodeError:
        await megadl.edit("**JSONDecodeError**: `failed to extract link...`")
        return None
    except (IndexError, TypeError):
        return
    file_name = data["file_name"]
    file_url = data["url"]
    hex_key = data["hex_key"]
    hex_raw_key = data["hex_raw_key"]
    temp_file_name = file_name + ".temp"
    temp_file_path = os.path.join(TEMP_DOWNLOAD_DIRECTORY, temp_file_name)
    file_path = os.path.join(TEMP_DOWNLOAD_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        try:
            raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), file_path)
        except FileExistsError as e:
            await megadl.edit(f"`{str(e)}`")
            return None
    downloader = SmartDL(file_url, temp_file_path, progress_bar=False)
    display_message = None
    try:
        downloader.start(blocking=False)
    except HTTPError as e:
        await megadl.edit(f"**HTTPError**: `{str(e)}`")
        return None
    start = time.time()
    while not downloader.isFinished():
        status = downloader.get_status().capitalize()
        total_length = downloader.filesize if downloader.filesize else None
        downloaded = downloader.get_dl_size()
        percentage = int(downloader.get_progress() * 100)
        speed = downloader.get_speed(human=True)
        estimated_total_time = round(downloader.get_eta())
        progress_str = "`{0}` | [{1}{2}] `{3}%`".format(
            status,
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        diff = time.time() - start
        try:
            current_message = (
                f"**➥file name : **`{file_name}`\n\n"
                "**➥Status**\n"
                f"{progress_str}\n"
                f"`{humanbytes(downloaded)}` of `{humanbytes(total_length)}`"
                f" @ `{speed}`\n"
                f"**➥ETA -> **`{time_formatter(estimated_total_time)}`\n"
                f"**➥ Duration -> **`{time_formatter(round(diff))}`"
            )
            if round(diff % 15.00) == 0 and (
                display_message != current_message or total_length == downloaded
            ):
                await megadl.edit(current_message)
                await asyncio.sleep(0.2)
                display_message = current_message
        except Exception:
            pass
        finally:
            if status == "Combining":
                wait = round(downloader.get_eta())
                await asyncio.sleep(wait)
    if downloader.isSuccessful():
        download_time = round(downloader.get_dl_time() + wait)
        try:
            P = multiprocessing.Process(
                target=await decrypt_file(
                    megadl, file_path, temp_file_path, hex_key, hex_raw_key
                ),
                name="Decrypt_File",
            )
            P.start()
            P.join()
        except FileNotFoundError as e:
            await megadl.edit(f"`{str(e)}`")
            return None
        else:
            await megadl.edit(
                f"**➥ file name : **`{file_name}`\n\n"
                f"**➥ Successfully downloaded in : ** `{file_path}`.\n"
                f"**➥ Download took :** {time_formatter(download_time)}."
            )
            return None
    else:
        await megadl.edit(
            "`Failed to download, " "check heroku Logs for more details.`"
        )
        for e in downloader.get_errors():
            LOGS.info(str(e))
    return


async def decrypt_file(megadl, file_path, temp_file_path, hex_key, hex_raw_key):
    cmd = "cat '{}' | openssl enc -d -aes-128-ctr -K {} -iv {} > '{}'".format(
        temp_file_path, hex_key, hex_raw_key, file_path
    )
    if await subprocess_run(megadl, cmd):
        os.remove(temp_file_path)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    return


CMD_HELP.update(
    {
        "downloads": ".gdl <gdrive File-Link>\
        \nUsage:G-Drive File Downloader Plugin For Userbot.\
        \n\n.mega <MEGA.nz link>\
        \nUsage: Reply to a MEGA.nz link or paste your MEGA.nz link to download the file into your userbot server."
    }
)
