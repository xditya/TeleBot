#  (c)2020 TeleBot
#
# You may not use this plugin without proper authorship and consent from @TeleBotSupport
#
from userbot.utils import admin_cmd, sudo_cmd
from userbot.uniborgConfig import Config
from userbot import telever, ALIVE_NAME
from heroku_config import Var
from userbot import bot

if Config.PRIVATE_GROUP_BOT_API_ID:
 log = "Enabled"
else:
 log = "Disabled"

if Config.TG_BOT_USER_NAME_BF_HER:
 bots = "Enabled"
else:
 bots = "Disabled"
 
if Var.LYDIA_API_KEY:
 lyd = "Enabled"
else:
 lyd = "Disabled"
 
if Config.SUDO_USERS:
 sudo = "Disabled"
else:
 sudo = "Enabled"
 
if Var.PMSECURITY.lower() == "off":
 pm = "Disabled" 
else:
 pm = "Enabled"
 
TELEUSER = str(ALIVE_NAME) if ALIVE_NAME else "@TeleBotSupport"

myid = bot.uid
tele = f"**TeleBot Stats for [{TELEUSER}](tg://user?id={myid})**\n\n"
tele +=f"**TeleBot Version**: {telever}\n"
tele +=f"**Log Group**: {log}\n"
tele +=f"**Assistant Bot**: {bots}\n"
tele +=f"**Lydia**: {lyd}\n"
tele +=f"**Sudo**: {sudo}\n"
tele +=f"**PMSecurity**: {pm}\n"
tele +=f"\nVisit @TeleBotSupport\nfor assistance.\n"
telestats = (f"{tele}")

"""
Usage - .stats - To see the variable stats of TeleBot {inline}
"""
