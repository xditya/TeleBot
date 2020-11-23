""" Powered by @Google
Available Commands:
.go <query> credits to owner of bot
"""

from re import findall

from search_engine_parser import GoogleSearch

from telebot import CMD_HELP


def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@telebot.on(admin_cmd(outgoing=True, pattern="go (.*)"))
async def gsearch(q_event):
    """ For .google command, do a Google search. """
    match = q_event.pattern_match.group(1)
    tele = await eor(q_event, "Searching for `{}`".format(match))
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
    res = ""
    for i in range(len(gresults["links"])):
        try:
            teletitle = gresults["titles"][i]
            telelink = gresults["links"][i]
            teledescrp = gresults["descriptions"][i]
            res += f"[{teletitle}]({telelink})\n`{teledescrp}`\n\n"
        except IndexError:
            break
    await tele.edit(
        "**GᴏᴏɢʟᴇSᴇᴀʀᴄʜ**\n__Qᴜᴇʀʏ:__\n `{}` \n\n**Rᴇsᴜʟᴛs:**\n {}".format(match, res),
        link_preview=False,
    )


CMD_HELP.update({"google": ".go <query>\nUse - Search the query on Google"})
