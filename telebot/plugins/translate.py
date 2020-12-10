"""
Google Translate
Available Commands:
.tr LanguageCode as reply to a message
.tr LangaugeCode | text to translate
"""

import emoji
from googletrans import Translator

from telebot import CMD_HELP, CMD_HNDLR


@telebot.on(admin_cmd(pattern="tr ?(.*)"))
@telebot.on(sudo_cmd(pattern="tr ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    x = await eor(event, "Translating...")
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "ml"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await x.edit(
            f"`{CMD_HNDLR}tr LanguageCode` as reply to a message.\nLanguage codes can be found [here](https://t.me/TeleBotHelpChat/22678)",
        )
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = """
**Tʀᴀɴsʟᴀᴛɪᴏɴ**

**{} ➟ {}**

`{}`""".format(
            translated.src, lan, after_tr_text
        )
        await x.edit(output_str)
    except Exception as exc:
        await x.edit(f"Error\n `{str(exc)}`")


CMD_HELP.update(
    {
        "translate": ".tr <LanguageCode> <reply to a message>\
        \nUse - Translate the replied text\
        \n\n.tr <LangaugeCode> | <text to translate>\
        \nUse - Translate the given text.\
        \n\nLanguage codes can be found [here](https://t.me/TeleBotHelpChat/22678)."
    }
)
