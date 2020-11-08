# credits to the respective devs
# ported by @its_xditya

from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from shutil import which

from telebot import ALIVE_NAME, CMD_HELP, telever

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot"
# ============================================


@telebot.on(admin_cmd(pattern="sysd"))
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@telebot.on(admin_cmd(pattern="version"))
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await event.edit(
                "`Telebot Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`"
            )
        else:
            await event.edit(
                f"Shame that you don't have git, you're running - {telever} anyway!"
            )


@telebot.on(admin_cmd(pattern="pip(?: |$)(.*)"))
async def pipcheck(pip):
    """ For .pip command, do a pip search. """
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            pipc = await asyncrunapp(
                "pip3",
                "search",
                pipmodule,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            if pipout:
                if len(pipout) > 4096:
                    await pip.edit("`Output too large, sending as file`")
                    file = open("output.txt", "w+")
                    file.write(pipout)
                    file.close()
                    await pip.client.send_file(
                        pip.chat_id,
                        "output.txt",
                        reply_to=pip.id,
                    )
                    remove("output.txt")
                    return
                await pip.edit(
                    "**Query: **\n`"
                    f"pip3 search {pipmodule}"
                    "`\n**Result: **\n`"
                    f"{pipout}"
                    "`"
                )
            else:
                await pip.edit(
                    "**Query: **\n`"
                    f"pip3 search {pipmodule}"
                    "`\n**Result: **\n`No Result Returned/False`"
                )
        else:
            await pip.edit("`Use .help pip to see an example`")


CMD_HELP.update(
    {
        "system": "➟ .sysd\nUsage: Shows system information using neofetch.\
        \n\n➟ .version\nUsage: Shows the userbot version.\
        \n\n➟ .pip <module(s)>\nUsage: Does a search of pip modules(s)."
    }
)
