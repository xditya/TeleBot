from userbot import bot
from sys import argv
from telethon import TelegramClient
from var import Var
from userbot.utils import load_module, start_mybot
from pathlib import Path
import telethon.utils
from userbot import CMD_HNDLR

async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me() 
    bot.uid = telethon.utils.get_peer_id(bot.me)

TELE = Var.PRIVATE_GROUP_ID
MYBOT = Var.TG_BOT_USER_NAME_BF_HER

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        print("Initiating Inline Bot")
        # ForTheGreatrerGood of beautification
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
        print("Initialisation finished, no errors")
        print("Starting Userbot")
        bot.loop.run_until_complete(add_bot(Var.TG_BOT_USER_NAME_BF_HER))
        print("Startup Completed")
    else:
        bot.start()
await telebot.send_message(TELE, "Deploying TeleBot...")    
import glob
path = 'userbot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
print("TeleBot has been deployed! ")
await telebot.send_message(TELE, "TeleBot has been deployed...")
print("Setting up TGBot")
await telebot.send_message(TELE, f"Setting up @{MYBOT}")
path = "userbot/plugins/mybot/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        start_mybot(shortname.replace(".py", ""))
print("TGBot has been set up!")      
await telebot.send_message(TELE, f"@{MYBOT} has been set up. Send ```/start``` to the bot 😁")")
print("TeleBot has been fully deployed! Do Visit @TeleBotSupport")
await telebot.send_message(TELE, f"TeleBot has been fully deployed. {MYBOT} has been set-up completely.")
await telebot.send_message(TELE, f"Send ```{CMD_HNDLR}alive``` to see if the bot is working.\n\nDo add @{MYBOT} to this group and make it admin, else some features won't work")
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()

