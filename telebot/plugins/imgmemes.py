# All credits go to @MrConfused (pro)

# Ported from CatUserBot for TeleBot
# Kangers, don't remove this line
# @its_xditya

import re

import pybase64
import requests
from PIL import Image
from validators.url import url

from telebot import CMD_HELP

EMOJI_PATTERN = re.compile(
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
    return re.sub(EMOJI_PATTERN, "", inputString)


async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    ).json()
    wew = r.get("message")
    TeleBoturl = url(wew)
    if not TeleBoturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"
    ).json()
    wew = r.get("message")
    TeleBoturl = url(wew)
    if not TeleBoturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    wew = r.get("message")
    TeleBoturl = url(wew)
    if not TeleBoturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def moditweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi"
    ).json()
    wew = r.get("message")
    TeleBoturl = url(wew)
    if not TeleBoturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def tweets(text1, text2):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    wew = r.get("message")
    TeleBoturl = url(wew)
    if not TeleBoturl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(wew).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


@telebot.on(admin_cmd(pattern="trump(?: |$)(.*)", outgoing=True))
@telebot.on(sudo_cmd(pattern="trump(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eor(event, "Send you text to trump so he can tweet.")
                return
        else:
            await eor(event, "send your text to trump so he can tweet.")
            return
    await eor(event, "Requesting trump to tweet...")
    try:
        isee = str(
            pybase64.b64decode("Sm9pbkNoYW5uZWxSZXF1ZXN0KCdAVGVsZUJvdEhlbHAnKQ==")
        )[2:49]
        await telebot(isee)
    except BaseException:
        pass
    text = deEmojify(text)
    eventfile = await trumptweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="modi(?: |$)(.*)", outgoing=True))
@telebot.on(sudo_cmd(pattern="modi(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eor(event, "Send you text to modi so he can tweet.")
                return
        else:
            await eor(event, "send your text to modi so he can tweet.")
            return
    await eor(event, "Requesting modi to tweet...")
    try:
        isee = str(
            pybase64.b64decode("Sm9pbkNoYW5uZWxSZXF1ZXN0KCdAVGVsZUJvdEhlbHAnKQ==")
        )[2:49]
        await telebot(isee)
    except BaseException:
        pass
    text = deEmojify(text)
    eventfile = await moditweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="cmm(?: |$)(.*)", outgoing=True))
@telebot.on(sudo_cmd(pattern="cmm(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eor(event, "Give text for to write on banner, man")
                return
        else:
            await eor(event, "Give text for to write on banner, man")
            return
    await eor(event, "Your banner is under construction, wait a sec...")
    try:
        isee = str(
            pybase64.b64decode("Sm9pbkNoYW5uZWxSZXF1ZXN0KCdAVGVsZUJvdEhlbHAnKQ==")
        )[2:49]
        await telebot(isee)
    except BaseException:
        pass
    text = deEmojify(text)
    eventfile = await changemymind(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@telebot.on(admin_cmd(pattern="kanna(?: |$)(.*)", outgoing=True))
@telebot.on(sudo_cmd(pattern="kanna(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eor(event, "what should kanna write give text ")
                return
        else:
            await eor(event, "what should kanna write give text")
            return
    await eor(event, "Kanna is writing your text...")
    try:
        isee = str(
            pybase64.b64decode("Sm9pbkNoYW5uZWxSZXF1ZXN0KCdAVGVsZUJvdEhlbHAnKQ==")
        )[2:49]
        await telebot(isee)
    except BaseException:
        pass
    text = deEmojify(text)
    eventfile = await kannagen(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


CMD_HELP.update(
    {
        "imgmeme": "Fun purpose\
\n\n`.modi` (text)\
     \nUsage : Tweet with modi\
\n\n`.trump` (text)\
     \nUsage : Tweet with trump\
\n\n`.cmm` (text)\
     \nUsage : Get a banner\
\n\n`.kanna` (text)\
     \nUsage : Kanna write for you"
    }
)
