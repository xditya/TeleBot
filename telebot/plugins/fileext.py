"""Get info about a File Extension
Syntax: .filext EXTENSION"""
import requests
from bs4 import BeautifulSoup
from uniborg.util import admin_cmd

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern="filext (.*)"))
@telebot.on(admin_cmd(pattern="filext (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await eor(event, "Processing ...")
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = requests.get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        await eor(
            event,
            "**File Extension**: `{}`\n**Description**: `{}`".format(
                input_str, ext_details
            ),
        )
    else:
        await eor(
            event,
            "https://www.fileext.com/ responded with {} for query: {}".format(
                status_code, input_str
            ),
        )


CMD_HELP.update(
    {"fileext": ".fileext <extension>\nUse - Get info on that file extension."}
)
