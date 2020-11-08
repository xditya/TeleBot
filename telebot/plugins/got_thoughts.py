# BY @Deonnn
"""
Game of Thrones Thoughts plugin
by @Deonnn
command .gott

"""


import asyncio
import random

from telebot import CMD_HELP
from telebot.utils import admin_cmd


@telebot.on(admin_cmd(pattern="gott", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    await eor(event, "Typing...")

    await asyncio.sleep(2)

    x = random.randrange(1, 40)

    if x == 1:

        await eor(event, '`"The man who passes the sentence should swing the sword."`')

    if x == 2:

        await eor(
            event,
            '`"When the snows fall and the white winds blow, the lone wolf dies but the pack survives!"`',
        )

    if x == 3:

        await eor(event, '`"The things I do for love!"`')

    if x == 4:

        await eor(
            event,
            '`"I have a tender spot in my heart for cripples, bastards and broken things."`',
        )

    if x == 5:

        await eor(
            event,
            '`"Death is so terribly final, while life is full of possibilities."`',
        )

    if x == 6:

        await eor(
            event,
            '`"Once you’ve accepted your flaws, no one can use them against you."`',
        )

    if x == 7:

        await eor(event, '`"If I look back I am lost."`')

    if x == 8:

        await eor(event, '`"When you play the game of thrones, you win or you die."`')

    if x == 9:

        await eor(
            event, '`"I grew up with soldiers. I learned how to die a long time ago."`'
        )

    if x == 10:

        await eor(event, '`"What do we say to the Lord of Death?\nNot Today!"`')

    if x == 11:

        await eor(event, '`"Every flight begins with a fall."`')

    if x == 12:

        await eor(event, '`"Different roads sometimes lead to the same castle."`')

    if x == 13:

        await eor(
            event,
            '`"Never forget what you are. The rest of the world will not. Wear it like armour, and it can never be used to hurt you."`',
        )

    if x == 14:

        await eor(
            event,
            '`"The day will come when you think you are safe and happy, and your joy will turn to ashes in your mouth."`',
        )

    if x == 15:

        await eor(event, '`"The night is dark and full of terrors."`')

    if x == 16:

        await eor(event, '`"You know nothing, Jon Snow."`')

    if x == 17:

        await eor(event, '`"Night gathers, and now my watch begins!"`')

    if x == 18:

        await eor(event, '`"A Lannister always pays his debts."`')

    if x == 19:

        await eor(event, '`"Burn them all!"`')

    if x == 20:

        await eor(event, '`"What do we say to the God of death?"`')

    if x == 21:

        await eor(event, '`"There\'s no cure for being a c*nt."`')

    if x == 22:

        await eor(event, '`"Winter is coming!"`')

    if x == 23:

        await eor(event, '`"That\'s what I do: I drink and I know things."`')

    if x == 24:

        await eor(
            event,
            '`"I am the dragon\'s daughter, and I swear to you that those who would harm you will die screaming."`',
        )

    if x == 25:

        await eor(
            event, '`"A lion does not concern himself with the opinion of sheep."`'
        )

    if x == 26:

        await eor(event, '`"Chaos isn\'t a pit. Chaos is a ladder."`')

    if x == 27:

        await eor(
            event,
            '`"I understand that if any more words come pouring out your c*nt mouth, I\'m gonna have to eat every f*cking chicken in this room."`',
        )

    if x == 28:

        await eor(
            event,
            '`"If you think this has a happy ending, you haven\'t been paying attention."`',
        )

    if x == 29:

        await eor(
            event,
            '`"If you ever call me sister again, I\'ll have you strangled in your sleep."`',
        )

    if x == 30:

        await eor(event, '`"A girl is Arya Stark of Winterfell. And I\'m going home."`')

    if x == 31:

        await eor(event, "`\"Any man who must say 'I am the King' is no true King.\"`")

    if x == 32:

        await eor(event, '`"If I fall, don\'t bring me back."`')

    if x == 33:

        await eor(
            event,
            "`\"Lannister, Targaryen, Baratheon, Stark, Tyrell... they're all just spokes on a wheel. This one's on top, then that one's on top, and on and on it spins, crushing those on the ground.\"`",
        )

    if x == 34:

        await eor(event, '`"Hold the door!`')

    if x == 35:

        await eor(
            event,
            '`"When people ask you what happened here, tell them the North remembers. Tell them winter came for House Frey."`',
        )

    if x == 36:

        await eor(event, '`"Nothing f*cks you harder than time."`')

    if x == 37:

        await eor(
            event,
            '`"There is only one war that matters. The Great War. And it is here."`',
        )

    if x == 38:

        await eor(event, '`"Power is power!"`')

    if x == 39:

        await eor(event, '`"I demand a trial by combat!"`')

    if x == 40:

        await eor(event, '`"I wish I was the monster you think I am!"`')


CMD_HELP.update({"got_thoughts": ".gott\nUse - Get random thoughts."})
