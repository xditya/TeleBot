"""CoronaVirus LookUp
Syntax: .coronavirus <country>"""
from covid import Covid

from telebot import CMD_HELP


@telebot.on(admin_cmd(pattern="coronavirus (.*)"))
@telebot.on(sudo_cmd(pattern="coronavirus (.*)", allow_sudo=True))
async def _(event):
    covid = Covid()
    data = covid.get_data()
    country = event.pattern_match.group(1)
    country_data = get_country_data(country, data)
    output_text = ""
    for name, value in country_data.items():
        output_text += "`{}`: `{}`\n".format(str(name), str(value))
    await eor(
        event,
        "**CoronaVirus Info in {}**:\n\n{}".format(country.capitalize(), output_text),
    )


def get_country_data(country, world):
    for country_data in world:
        if country_data["country"].lower() == country.lower():
            return country_data
    return {"Status": "No information yet about this country!"}


CMD_HELP.update(
    {
        "coronavirus": ".coronavirus <country name>\nUse - Get covid status of that country"
    }
)
