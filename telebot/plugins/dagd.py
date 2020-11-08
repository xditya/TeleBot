"""DA.GD helpers in @UniBorg
Available Commands:
.isup URL
.dns google.com
.url <long url>
.unshort <short url>"""
import requests

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="dns (.*)"))
@telebot.on(sudo_cmd(pattern="dns (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(event, "DNS records of {} are \n{}".format(input_str, response_api))
    else:
        await eor(event, "i can't seem to find {} on the internet".format(input_str))


@telebot.on(admin_cmd(pattern="url (.*)"))
@telebot.on(sudo_cmd(pattern="url (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(event, "Generated {} for {}.".format(response_api, input_str))
    else:
        await eor(event, "something is wrong. please try again later.")


@telebot.on(admin_cmd(pattern="unshort (.*)"))
@telebot.on(sudo_cmd(pattern="unshort (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await eor(
            event,
            "Input URL: {}\nReDirected URL: {}".format(
                input_str, r.headers["Location"]
            ),
        )
    else:
        await eor(
            event,
            "Input URL {} returned status_code {}".format(input_str, r.status_code),
        )


CMD_HELP.update(
    {
        "dagd": ".dns\nUse - Find DNS records.\
        \n\n.url <link>\nUse - Shorten the link via da.gd\
        \n\n.unshort <link>\nUse - UnShorten the URL."
    }
)
