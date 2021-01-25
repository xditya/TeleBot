# Author: Shubhendra Kushwaha (@TheShubhendra)
# Email: shubhendrakushwaha94@gmail.com
import pygita

from telebot import CMD_HELP
from telebot.utils import admin_cmd

CLIENT_ID = Config.GITA_CLIENT_ID
CLIENT_SECRET = Config.GITA_CLIENT_SECRET
"""Get API crendentials from https://bhagavadgita.io."""


@telebot.on(admin_cmd(pattern="gita +(.*) +(.*)$"))
async def gita(event):
    """To get a specific verse from a specific chapter in English."""
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await event.edit(
            "`Please add required GITA_CLIENT_SECRET and GITA_CLIENT_ID env var`"
        )
        return
    pygita.auth(CLIENT_ID, CLIENT_SECRET)
    try:
        chapter_number = int(event.pattern_match.group(1))
        verse_number = int(event.pattern_match.group(2))
    except ValueError:
        return
    verse = pygita.get_verse(chapter_number, verse_number, language="en")
    await event.edit(f"**{verse.text}** {verse.meaning}")


@telebot.on(admin_cmd(pattern="gita +(.*) +(.*) hi$"))
async def gita_hindi(event):
    """To get a specific verse from a specific chapter in Hindi."""
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await event.edit(
            "`Please add required GITA_CLIENT_SECRET and GITA_CLIENT_ID env var`"
        )
        return
    pygita.auth(CLIENT_ID, CLIENT_SECRET)
    chapter_number = int(event.pattern_match.group(1))
    verse_number = int(event.pattern_match.group(2))
    verse = pygita.get_verse(chapter_number, verse_number, language="hi")
    await event.edit(f"**{verse.text}** {verse.meaning}")


CMD_HELP.update(
    {
        "gita": "**gita**\
\n\n**Syntax : **`.verse <chapter_number> <verse_number>`\
\n**Usage :** Get a specific verse from a particular chapter\
\n\n**Syntax : **`.verse <chapter_number> <verse_number> hi`\
\n**Usage :** Get a specific verse from a particular chapter in hindi.\n"
    }
)
