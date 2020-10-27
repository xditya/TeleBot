# Join @TeleBotHelp for custom plugins

import asyncio

from telebot.utils import admin_cmd, sudo_cmd


@telebot.on(admin_cmd(pattern="cmds", outgoing=True))
@telebot.on(sudo_cmd(pattern="cmds", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    cmd = "ls userbot/plugins"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
    OUTPUT = f"**List of Plugins:**\n`{o}`\n\n**TIP:** __If you want to know the commands for a plugin, do:-__ \n `.help <plugin name>` **without the < > brackets.**\n__All plugins might not work directly.\n (c)TeleBot."
    await eor(event, OUTPUT)
