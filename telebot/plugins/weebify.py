""" Weebify a text,
# For TeleBot
By :- @PhycoNinja13b
Modified by :- @kirito6969
.weeb <text> """

from telebot.utils import admin_cmd

normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


@telebot.on(admin_cmd(pattern="weeb ?(.*)"))
@telebot.on(sudo_cmd(pattern="weeb ?(.*)", allow_sudo=True))
async def weebify(event):

    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await eor(event, "`What I am Supposed to Weebify U Dumb`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await eor(event, string)
