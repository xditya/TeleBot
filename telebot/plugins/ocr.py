import os

import requests

from telebot import CMD_HELP, OCR_SPACE_API_KEY, TEMP_DOWNLOAD_DIRECTORY, bot
from telebot.utils import admin_cmd


async def ocr_space_file(
    filename, overlay=False, api_key=OCR_SPACE_API_KEY, language="eng"
):
    """OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.json()


@telebot.on(admin_cmd(pattern="ocr(?: |$)(.*)", outgoing=True))
@telebot.on(sudo_cmd(pattern="ocr(?: |$)(.*)", allow_sudo=True))
async def ocr(event):
    await eor(event, "`Reading...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY
    )
    test_file = await ocr_space_file(filename=downloaded_file_name, language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await eor(event, "`Couldn't read it.`\nTry using `.ocr eng`")
    else:
        await eor(event, f"`Here's what I could read from it:`\n\n{ParsedText}")
    os.remove(downloaded_file_name)


CMD_HELP.update(
    {
        "ocr": ".ocr <language>\nUsage: Reply to an image or sticker to extract text from it.\n\nGet language codes from [here](https://ocr.space/ocrapi)"
    }
)
