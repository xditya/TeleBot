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

from telethon import events, Button
from userbot.plugins.mybot import started, helpmefast, forping
import html
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
import emoji
from googletrans import Translator
import heroku3
import asyncio
import os
import requests
import math
from telethon import events, Button
from userbot import ALIVE_NAME
from telebotConfig import Var
from userbot import bot

DEF = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot"


@tgbot.on(events.NewMessage(pattern="^/start"))
async def thisfn(event):
    await tgbot.send_message(
        event.chat_id,
        message=started,
        buttons=[
            [Button.url("Repository", "https://github.com/xditya/TeleBot/")]
        ]
    )


@tgbot.on(events.NewMessage(pattern="^/help"))
async def thisfn(event):
    await tgbot.send_message(
        event.chat_id,
        message=helpmefast,
        link_preview=False,
        buttons=[
            [Button.url("TeleBot", "https://t.me/TeleBotSupport")]
        ]
    )


@tgbot.on(events.NewMessage(pattern="^/ping"))
async def thisfn(event):
    await tgbot.send_message(
        event.chat_id,
        message=forping,
        buttons=[
            [Button.url("Deploy", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot")]
        ]
    )


@tgbot.on(events.NewMessage(pattern="^/info ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    replied_user_profile_photos = await event.client(GetUserPhotosRequest(
        user_id=replied_user.user.id,
        offset=42,
        max_id=0,
        limit=80
    ))
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Need a Profile Picture to check **this**"
        str(e)
    caption = """Extracted Userdata From TeleBot's DATABASE
ID: <code>{}</code>
Target's Name: <a href='tg://user?id={}'>{}</a>
Bio: {}
DC ID: {}
Number of PPs: {}
Restricted? : {}
Verified : {}
Bot : {}
No. of Common Groups : {}
""".format(
        user_id,
        user_id,
        first_name,
        user_bio,
        dc_id,
        replied_user_profile_photos_count,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await tgbot.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
        buttons=[
            [Button.url("More", "https://t.me/TeleBotSupport")]
        ]
    )


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


@tgbot.on(events.NewMessage(pattern="^/tr ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "ml"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.edit("`.tr LanguageCode` as reply to a message")
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = """**Translated by TeleBot**\nFrom {} to {}
{}""".format(
            translated.src,
            lan,
            after_tr_text
        )
        await tgbot.send_message(
            event.chat_id,
            message=output_str,
            buttons=[
                [Button.url("More", "https://t.me/TeleBotSupport")]
            ]
        )
    except Exception as exc:
        xx = str(exc)
        await tgbot.send_message(
            event.chat_id,
            message=xx,
            buttons=[
                [Button.url("More", "https://t.me/TeleBotSupport")]
            ]
        )


@tgbot.on(events.NewMessage(pattern="^/id"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            tosend = "Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(
                str(event.chat_id), str(r_msg.from_id), bot_api_file_id)
            await tgbot.send_message(
                event.chat_id,
                message=tosend,
                buttons=[
                    [Button.url("More", "https://t.me/TeleBotSupport")]
                ]
            )
        else:
            sendit = "Current Chat ID: `{}`\nFrom User ID: `{}`".format(
                str(event.chat_id), str(r_msg.from_id))
            await tgbot.send_message(
                event.chat_id,
                message=sendit,
                buttons=[
                    [Button.url("More", "https://t.me/TeleBotSupport")]
                ]
            )
    else:
        kek = "Current Chat ID: `{}`".format(str(event.chat_id))
        await tgbot.send_message(
            event.chat_id,
            message=kek,
            buttons=[
                [Button.url("More", "https://t.me/TeleBotSupport")]
            ]
        )

Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"


@tgbot.on(events.NewMessage(pattern=r"^/usage(?: |$)"))
async def dyno_usage(dyno):
    """
        Get your account Dyno Usage
    """
    if dyno.from_id == bot.uid:
        await dyno.edit("`Processing...`")
        useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/80.0.3987.149 Mobile Safari/537.36'
                     )
        user_id = Heroku.account().id
        headers = {
            'User-Agent': useragent,
            'Authorization': f'Bearer {Var.HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        if r.status_code != 200:
            return await dyno.edit("`Error: something bad happened`\n\n"
                                   f">.`{r.reason}`\n")
        result = r.json()
        quota = result['account_quota']
        quota_used = result['quota_used']

        """ - Used - """
        remaining_quota = quota - quota_used
        percentage = math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)

        """ - Current - """
        App = result['apps']
        try:
            App[0]['quota_used']
        except IndexError:
            AppQuotaUsed = 0
            AppPercentage = 0
        else:
            AppQuotaUsed = App[0]['quota_used'] / 60
            AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)

        await asyncio.sleep(1.5)

        return await tgbot.send_message(dyno.chat_id, "**⚙️ Dyno Usage ⚙️**:\n\n"
                                        f" -> `Dyno usage for`  **{Var.HEROKU_APP_NAME}**:\n"
                                        f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                                        f"**|**  [`{AppPercentage}`**%**]"
                                        "\n\n"
                                        " -> `Dyno hours quota remaining this month`:\n"
                                        f"     •  `{hours}`**h**  `{minutes}`**m**  "
                                        f"**|**  [`{percentage}`**%**]"
                                        )
    else:
        resp = f"This option is available only for my master, {DEF}!"
        return await tgbot.send_message(dyno.chat_id, message=resp, buttons=[
            [Button.url("Deploy Your TeleBot", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot")]
        ])


@tgbot.on(events.NewMessage(pattern=r"^/logs"))
async def _(givelogs):
    Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
    app = Heroku.app(Var.HEROKU_APP_NAME)
    with open('logs.txt', 'w') as log:
        log.write(app.get_log())
    if givelogs.from_id == bot.uid:
        await tgbot.send_file(
            givelogs.chat_id,
            "logs.txt",
            reply_to=givelogs.id,
            caption="[Heroku] TeleBot Logs",
            buttons=[
                [Button.url("Crashed?", "t.me/TeleBotHelpChat")]
            ])
    else:
        resp = f"This option is available only for my master, {DEF}!"
        await tgbot.send_message(givelogs.chat_id, message=resp, buttons=[
            [Button.url("Deploy Your TeleBot", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot&template=https%3A%2F%2Fgithub.com%2Fxditya%2FTeleBot")]
        ])
    await asyncio.sleep(5)
    return os.remove('logs.txt')
