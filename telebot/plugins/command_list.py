# Join @TeleBotHelp for custom plugins

import asyncio

from telegraph import Telegraph

from telebot import CMD_HELP

telegraph = Telegraph()
mee = telegraph.create_account(short_name="telebot")


@telebot.on(admin_cmd(pattern="cmds", outgoing=True))
@telebot.on(sudo_cmd(pattern="cmds", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    x = await eor(event, "Making a list of all plugins...")
    cmd = "ls telebot/plugins"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await x.edit("Pasting it to telegraph")
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
    OUTPUT = f"Here is the list of plugins found in 'master' branch of TeleBot.\n{o}\n\nUse .help <cmd_name> to learn how a paticular plugin works.\nConsider joining @TeleBotSupport for help!"
    title = "TeleBot Plugins List."
    topaste = OUTPUT.text
    topaste = topaste.replace("\n", "<br>")
    response = telegraph.create_page(title, html_content=topaste)
    link = response["path"]
    tele = f"All the plugins of TeleBot can be found [here](telegra.ph/{link})"
    await x.edit(tele, link_preview=False)


CMD_HELP.update(
    {
        "command_list": ".cmds\nUse - To get a list of all plugins installed in the userbot."
    }
)
