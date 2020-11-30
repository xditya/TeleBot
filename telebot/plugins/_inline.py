#    TeleBot - UserBot
#    Copyright (C) 2020 TeleBot

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import html
import os
import re
from math import ceil

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest

from telebot import ALIVE_NAME, CMD_HELP, CMD_LIST, CUSTOM_PMPERMIT, bot
from telebot.plugins import telestats
from telebot.telebotConfig import Var

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
TELEPIC = (
    PMPERMIT_PIC
    if PMPERMIT_PIC
    else "https://telegra.ph/file/92cfbab6598148837c2e4.jpg"
)
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
myid = bot.uid
mybot = Var.TG_BOT_USER_NAME_BF_HER
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Var.PRIVATE_GROUP_ID
MESAG = (
    str(CUSTOM_PMPERMIT)
    if CUSTOM_PMPERMIT
    else "`TeleBot PM security! Please wait for me to approve you. 😊"
)
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot User"
USER_BOT_WARN_ZERO = "`I had warned you not to spam. Now you have been blocked and reported until further notice.`\n\n**GoodBye!** "

if Var.LOAD_MYBOT == "True":
    USER_BOT_NO_WARN = (
        "**PM Security of [{}](tg://user?id={})**\n\n"
        "{}\n\n"
        "For immediate help, PM me via {}"
        "\nPlease choose why you are here, from the available options\n\n".format(
            DEFAULTUSER, myid, MESAG, botname
        )
    )
elif Var.LOAD_MYBOT == "False":
    USER_BOT_NO_WARN = (
        "**PM Security of [{}](tg://user?id={})**\n\n"
        "{}\n"
        "\nPlease choose why you are here, from the available options\n".format(
            DEFAULTUSER, myid, MESAG
        )
    )

CUSTOM_HELP_EMOJI = os.environ.get("CUSTOM_HELP_EMOJI", "⚡")
HELP_ROWS = int(os.environ.get("HELP_ROWS", 5))
HELP_COLOUMNS = int(os.environ.get("HELP_COLOUMNS", 3))

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("`Userbot"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")
            result = builder.article(
                "© TeleBot Help",
                text="{}\nCurrently Loaded Plugins: {}".format(query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query == "stats":
            result = builder.article(
                title="Stats",
                text=f"**TeleBot Stats For [{DEFAULTUSER}](tg://user?id={myid})**\n\n__Bot is functioning normally, master!__\n\n(c) @TeleBotSupport",
                buttons=[
                    [custom.Button.inline("Stats", data="statcheck")],
                    [Button.url("Repo", "https://github.com/xditya/TeleBot")],
                    [
                        Button.url(
                            "Deploy Now!",
                            "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot",
                        )
                    ],
                ],
            )
        elif event.query.user_id == bot.uid and query.startswith("**PM"):
            TELEBT = USER_BOT_NO_WARN.format(DEFAULTUSER, myid, MESAG)
            result = builder.photo(
                file=TELEPIC,
                text=TELEBT,
                buttons=[
                    [
                        custom.Button.inline("Request ", data="req"),
                        custom.Button.inline("Chat 💭", data="chat"),
                    ],
                    [custom.Button.inline("To spam 🚫", data="heheboi")],
                    [custom.Button.inline("What is this ❓", data="pmclick")],
                ],
            )
        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"TeleBot - Telegram Userbot.",
                buttons=[
                    [
                        Button.url("Repo", "https://github.com/xditya/TeleBot"),
                        Button.url(
                            "Deploy",
                            "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot",
                        ),
                    ],
                    [Button.url("Support", "https://t.me/TeleBotSupport")],
                ],
            )
        else:
            result = builder.article(
                "Source Code",
                text="**Welcome to TeleBot**\n\n`Click below buttons for more`",
                buttons=[
                    [custom.Button.url("Creator👨‍🦱", "https://t.me/its_xditya")],
                    [
                        custom.Button.url(
                            "👨‍💻Source Code‍💻", "https://github.com/xditya/TeleBot"
                        ),
                        custom.Button.url(
                            "Deploy 🌀",
                            "https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot",
                        ),
                    ],
                    [
                        custom.Button.url(
                            "Updates and Support Group↗️", "https://t.me/TeleBotSupport"
                        )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_next\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = (
                "Please get your own Userbot from @TeleBotHelp , and don't use mine!"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"This is the PM Security for {DEFAULTUSER} to keep away spammers and retards.\n\nProtected by [TeleBot](t.me/TeleBotSupport)"
            )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"reopen")))
    async def megic(event):
        if event.query.user_id == bot.uid:
            buttons = paginate_help(0, CMD_LIST, "helpme")
            await event.edit("Menu Re-opened", buttons=buttons)
        else:
            reply_pop_up_alert = "This bot ain't for u!!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Okay, `{DEFAULTUSER}` would get back to you soon!\nTill then please **wait patienly and don't spam here.**"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {DEFAULTUSER}, [{first_name}](tg://user?id={ok}) is **requesting** something in PM!"
            await tgbot.send_message(LOG_GP, tosend)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oho, you want to chat...\nPlease wait and see if {DEFAULTUSER} is in a mood to chat, if yes, he will be replying soon!\nTill then, **do not spam.**"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {DEFAULTUSER}, [{first_name}](tg://user?id={ok}) wants to PM you for **Random Chatting**!"
            await tgbot.send_message(LOG_GP, tosend)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"plshelpme")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oh!\n{DEFAULTUSER} would be glad to help you out...\nPlease leave your message here **in a single line** and wait till I respond 😊"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {DEFAULTUSER}, [{first_name}](tg://user?id={ok}) wants to PM you for **help**!"
            await tgbot.send_message(LOG_GP, tosend)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oh, so you are here to spam 😤\nGoodbye.\nYour message has been read and successfully ignored."
            )
            await borg(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await tgbot.send_message(
                LOG_GP,
                f"[{first_name}](tg://user?id={ok}) tried to **spam** your inbox.\nHenceforth, **blocked**",
            )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit(
                "Menu Closed!!", buttons=[Button.inline("Re-open Menu", data="reopen")]
            )
        else:
            reply_pop_up_alert = "Please get your own userbot from @TeleBotSupport "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"statcheck")))
    async def rip(event):
        text = telestats
        await event.answer(text, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_prev\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_LIST, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own Userbot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            plugin_name = event.data_match.group(1).decode("UTF-8")
            help_string = ""
            help_string += f"Commands Available in {plugin_name} - \n"
            try:
                if plugin_name in CMD_HELP:
                    for i in CMD_HELP[plugin_name]:
                        help_string += i
                    help_string += "\n"
                else:
                    for i in CMD_LIST[plugin_name]:
                        help_string += i
                        help_string += "\n"
            except BaseException:
                pass
            if help_string == "":
                reply_pop_up_alert = "{} has no detailed info.\nUse .help {}".format(
                    plugin_name, plugin_name
                )
            else:
                reply_pop_up_alert = help_string
            reply_pop_up_alert += "\n Use .unload {} to remove this plugin\n\
                © Telebot".format(
                plugin_name
            )
            if len(help_string) >= 140:
                oops = "List too long!\nCheck your saved messages!"
                await event.answer(oops, cache_time=0, alert=True)
                help_string += "\n\nThis will be auto-deleted in 1 minute!"
                if bot is not None and event.query.user_id == bot.uid:
                    ok = await bot.send_message("me", help_string)
                    await asyncio.sleep(60)
                    await ok.delete()
            else:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            reply_pop_up_alert = "Please get your own Userbot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = HELP_ROWS
    number_of_cols = HELP_COLOUMNS
    tele = CUSTOM_HELP_EMOJI
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{} {} {}".format(tele, x, tele), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⫷ Previous", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline("║ Close ║", data="close"),
                custom.Button.inline(
                    "Next ⫸", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


async def userinfo(event):
    target = await event.client(GetFullUserRequest(event.query.user_id))
    first_name = html.escape(target.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    return first_name
