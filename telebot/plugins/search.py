"""
UserBot Module to search the internet
All-in-one by @its_xditya
(c)TeleBot

Available commands:
.ggl - howtogoogle
.duckduckgo - search on duckduckgo
.go - search on google
"""

from re import findall

import requests
from search_engine_parser import GoogleSearch

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(outgoing=True, pattern=r"gs (.*)"))
@telebot.on(sudo_cmd(allow_sudo=True, pattern=r"gs (.*)"))
async def gsearch(q_event):
    """ For .google command, do a Google search from @TeleBotHelp. """
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await eor(
        q_event,
        "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg,
        link_preview=False,
    )


@telebot.on(admin_cmd("duckduckgo (.*)"))
@telebot.on(sudo_cmd("duckduckgo (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://duckduckgo.com/?q={}".format(input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await eor(
            event,
            "Let me 🦆 DuckDuckGo that for you:\n🔎 [{}]({})".format(input_str, link),
        )
    else:
        await eor(event, "something is wrong. please try again later.")


@telebot.on(admin_cmd(pattern="ggl (.*)"))
@telebot.on(sudo_cmd(pattern="ggl (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "[{}]({})\n`Thank me Later 🙃` ".format(input_str, response_api.rstrip()),
        )
    else:
        await eor(event, "something is wrong. please try again later.")


CMD_HELP.update(
    {
        "search": ".gs <query>\nUse - Google the query.\
        \n\n.duckduckgo <query>\nUse - Search on DuckDuckGo\
        \n\n.ggl <query>\nUse - Learn to search, lol."
    }
)
