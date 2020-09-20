#  (c)2020 TeleBot
#
# You may not use this plugin without proper authorship and consent from @TeleBotSupport
#
from userbot.utils import admin_cmd, sudo_cmd
from userbot.uniborgConfig import Config
from userbot import telever, ALIVE_NAME
from heroku_config import Var

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
 sudo = "Enabled"
else:
 sudo = "Disabled"
 
TELEUSER = str(ALIVE_NAME) if ALIVE_NAME else "@TeleBotSupport"
@telebot.on(admin_cmd(outgoing=True, pattern="stats"))
@telebot.on(sudo_cmd(outgoing=True, pattern="stats", allow_sudo=True))
async def telestats(stats):
 myid = bot.uid
 tele = f"**TeleBot Stats for [{TELEUSER}](tg://user?id={myid})**\n\n"
 tele +=f"**TeleBot Version**: {telever}\n"
 tele +=f"**Log Group**: {log}\n"
 tele +=f"**Assistant Bot**: {bots}\n"
 tele +=f"**Lydia**: {lyd}\n"
 tele +=f"**Sudo**: {sudo}\n"
 tele +=f"\nVisit @TeleBotSupport\nfor assistance.\n"
 chat = await stats.get_chat()
 await borg.send_message(stats.chat_id, tele)
 await stats.delete()

"""
Usage - .stats - To see the variable stats
"""
