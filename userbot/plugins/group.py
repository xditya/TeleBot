from userbot.utils import register

@register(outgoing=True, pattern="^.group$")

async def join(e):

    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):

        await e.edit("This is my community.\n\n[Channel](http://t.me/giveaways_24hrs)\n\n[Chat Group](http://t.me/giveaways24hrsdiscuss)\n\n[UserBot Tutorial](https://t.me/TeleBotHelp)")
