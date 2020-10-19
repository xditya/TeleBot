"""
Say something interesting...
Syntax: .belo
    by @Deonnn
Quotes credits: Being logical Channel
"""

import asyncio
import random

from userbot.utils import admin_cmd


@telebot.on(admin_cmd(pattern=r"belo", outgoing=True))
@telebot.on(sudo_cmd(pattern=r"belo"))
async def _(event):

    if event.fwd_from:

        return

    await event.eor("Typing...")

    await asyncio.sleep(2)

    x = random.randrange(1, 96)

    if x == 1:

        await event.eor(
            '`"Underwater bubbles and raindrops are total opposites of each other."`'
        )

    if x == 2:

        await event.eor(
            '`"If you buy an eraser you are literally paying for your mistakes."`'
        )

    if x == 3:

        await event.eor(
            '`"The Person you care for most has the potential to destroy you the most."`'
        )

    if x == 4:

        await event.eor(
            '`"If humans colonize the moon, it will probably attract retirement homes as the weaker gravity will allow the elderly to feel stronger."`'
        )

    if x == 5:

        await event.eor(
            '`"Any video with “wait for it” in the title is simply too long."`'
        )

    if x == 6:

        await event.eor(
            '`"Your age in years is how many times you’ve circled the Sun, but your age in months is how many times the Moon has circled you."`'
        )

    if x == 7:

        await event.eor(
            '`"Biting your tongue while eating is a perfect example of how you can still screw up, even with decades of experience."`'
        )

    if x == 8:

        await event.eor(
            '`"Saying that your home is powered by a wireless Nuclear fusion reactor that is 93 Million miles away sounds way cooler than just saying you have solar panels on your roof."`'
        )

    if x == 9:

        await event.eor(
            '`"The most crushing feeling is when someone smiles at you on the street and you don’t react fast enough to smile back."`'
        )

    if x == 10:

        await event.eor(
            '`"Teeth constantly require maintenance to prevent their decay when alive, and yet they manage to survive for thousands of years buried as fossils."`'
        )

    if x == 11:

        await event.eor('`"A folder is for things that you don\'t want to fold."`')

    if x == 12:

        await event.eor(
            '`"Waking up in the morning sometimes feels like resuming a shitty movie you decided to quit watching."`'
        )

    if x == 13:

        await event.eor(
            '`"If everything goes smoothly, you probably won\'t remember today."`'
        )

    if x == 14:

        await event.eor(
            '`"When you meet new people in real life, you unlock more characters for your dream world."`'
        )

    if x == 15:

        await event.eor(
            '`"Maybe if they renamed sunscreen to “anti-cancer cream” more people would wear it."`'
        )

    if x == 16:

        await event.eor(
            '`"200 years ago, people would never have guessed that humans in the future would communicate by silently tapping on glass."`'
        )

    if x == 17:

        await event.eor(
            '`"Parents worry about what their sons download and worry about what their daughters upload."`'
        )

    if x == 18:

        await event.eor(
            '`"It\'s crazy how you can be the same age as someone, but at a completely different stage in your life."`'
        )

    if x == 19:

        await event.eor(
            "`\"When you think you wanna die, you really don't wanna die, you just don't wanna live like this.\"`"
        )

    if x == 20:

        await event.eor('`"Technically, no one has ever been in an empty room."`')

    if x == 21:

        await event.eor(
            '`"An onion is the bass player of food. You would probably not enjoy it solo, but you’d miss it if it wasn’t there."`'
        )

    if x == 22:

        await event.eor(
            "`\"We run everywhere in videogames because we're too lazy to walk, but In real life we walk everywhere because we're too lazy to run.\"`"
        )

    if x == 23:

        await event.eor(
            '`"Every single decision you ever made has brought you to read this sentence."`'
        )

    if x == 24:

        await event.eor("`\"The word 'quiet' is often said very loud.\"`")

    if x == 25:

        await event.eor(
            '`"Everybody wants you to work hard, but nobody wants to hear about how hard you work."`'
        )

    if x == 26:

        await event.eor(
            '`"We brush our teeth with hair on a stick and brush our hair with teeth on a stick."`'
        )

    if x == 27:

        await event.eor(
            '`"No one remembers your awkward moments but they’re too busy remembering their own."`'
        )

    if x == 28:

        await event.eor(
            '`"Dumb people try to say simple ideas as complex as possible while smart people try to say complex ideas as simple as possible."`'
        )

    if x == 29:

        await event.eor(
            "`\"Some people think they're better than you because they grew up richer. Some people think they're better than you because they grew up poorer.\"`"
        )

    if x == 30:

        await event.eor(
            '`"The biggest irony is that computers & mobiles were invented to save out time!"`'
        )

    if x == 31:

        await event.eor(
            '`"After honey was first discovered, there was likely a period where people were taste testing any available slime from insects."`'
        )

    if x == 32:

        await event.eor(
            '`"You know you’re getting old when your parents start disappointing you, instead of you disappointing them."`'
        )

    if x == 33:

        await event.eor(
            '`"Humans are designed to learn through experience yet the education system has made it so we get no experience."`'
        )

    if x == 34:

        await event.eor(
            '`"By focusing on blinking, you blink slower... Same for breathing."`'
        )

    if x == 35:

        await event.eor(
            '`"Drivers in a hurry to beat traffic usually cause the accidents which create the traffic they were trying to avoid."`'
        )

    if x == 36:

        await event.eor(
            '`"Characters that get married in fiction were literally made for each other."`'
        )

    if x == 37:

        await event.eor(
            '`"Babies are a clean hard drive that can be programmed with any language."`'
        )

    if x == 38:

        await event.eor(
            "`\"There could be a miracle drug that cures every disease to man, that we'll never know about because it doesn't work on rats.\"`"
        )

    if x == 39:

        await event.eor(
            "`\"Rhinos evolved to grow a horn for protection, but it's what's making them go extinct.\"`"
        )

    if x == 40:

        await event.eor(
            '`"Maybe we don\'t find time travelers because we all die in 25-50 years."`'
        )

    if x == 41:

        await event.eor(
            '`"Sleep is the trial version of death, It even comes with ads based on your activity."`'
        )

    if x == 42:

        await event.eor(
            '`"The most unrealistic thing about Spy movies is how clean the air ventilation system is!"`'
        )

    if x == 43:

        await event.eor(
            '`"In games we play through easy modes to unlock hard modes. In life we play through hard modes to unlock easy modes."`'
        )

    if x == 44:

        await event.eor(
            '`"Silent people seem smarter than loud people, because they keep their stupid thoughts to themselves."`'
        )

    if x == 45:

        await event.eor('`"If Greenland actually turns green, we\'re all screwed."`')

    if x == 46:

        await event.eor(
            '`"If someone says clever things in your dream, it actually shows your own cleverness."`'
        )

    if x == 47:

        await event.eor(
            '`"Famous movie quotes are creored to the actor and not the actual writer who wrote them."`'
        )

    if x == 48:

        await event.eor(
            '`"No one actually teaches you how to ride a bicycle. They just hype you up until you work it out."`'
        )

    if x == 49:

        await event.eor('`"Ask yourself why the the brain ignores the second the."`')

    if x == 50:

        await event.eor(
            '`"You’ve probably forgot about 80% of your entire life and most of the memories you do remember are not very accurate to what actually happened."`'
        )

    if x == 51:

        await event.eor(
            '`"It will be a lot harder for kids to win against their parents in video games in the future."`'
        )

    if x == 52:

        await event.eor(
            '`"Everyone has flaws, if you don\'t recognize yours, you have a new one."`'
        )

    if x == 53:

        await event.eor('`"Raising a child is training your replacement."`')

    if x == 54:

        await event.eor(
            "`\"'O'pen starts with a Closed circle, and 'C'lose starts with an open circle.\"`"
        )

    if x == 55:

        await event.eor(
            '`"There\'s always someone who hated you for no reason, and still does."`'
        )

    if x == 56:

        await event.eor(
            '`"After popcorn was discovered, there must have been a lot of random seeds that were roasted to see if it would have the same effect."`'
        )

    if x == 57:

        await event.eor(
            '`"The more important a good night\'s sleep is, the harder it is to fall asleep."`'
        )

    if x == 58:

        await event.eor(
            '`"Blessed are those that can properly describe the type of haircut they want to a new stylist."`'
        )

    if x == 59:

        await event.eor(
            "`\"Too many people spend money they haven't earned, to buy things they don't want, to impress people they don't like!\"`"
        )

    if x == 60:

        await event.eor(
            '`"Theme park employees must be good at telling the difference between screams of horror and excitement."`'
        )

    if x == 61:

        await event.eor('`"6 to 6:30 feels more half-an-hour than 5:50 to 6:20"`')

    if x == 62:

        await event.eor(
            '`"Getting your password right on the last login attempt before lockout is the closest thing to disarming a bomb at the last minute that most of us will experience."`'
        )

    if x == 63:

        await event.eor(
            '`"Listening to podcasts before bed is the adult version of story-time."`'
        )

    if x == 64:

        await event.eor(
            '`"If all criminals stopped robbing then the security industry would fall in which they could then easily go back to robbing."`'
        )

    if x == 65:

        await event.eor('`"A ton of whales is really only like half a whale."`')

    if x == 66:

        await event.eor(
            '`"When you get old, the old you is technically the new you, and your young self is the old you."`'
        )

    if x == 67:

        await event.eor(
            '`"You probably won\'t find many negative reviews of parachutes on the Internet."`'
        )

    if x == 68:

        await event.eor(
            '`"We show the most love and admiration for people when they\'re no longer around to appreciate it."`'
        )

    if x == 69:

        await event.eor(
            "`\"We've practiced sleeping thousands of times, yet can't do it very well or be consistent.\"`"
        )

    if x == 70:

        await event.eor(
            '`"Humans are more enthusiastic about moving to another planet with hostile environment than preserving earth - the planet they are perfectly shaped for."`'
        )

    if x == 71:

        await event.eor(
            "`\"The happiest stage of most people's lives is when their brains aren't fully developed yet.\"`"
        )

    if x == 72:

        await event.eor('`"The most effective alarm clock is a full bladder."`')

    if x == 73:

        await event.eor(
            '`"You probably just synchronized blinks with millions of people."`'
        )

    if x == 74:

        await event.eor(
            '`"Since we test drugs on animals first, rat medicine must be years ahead of human medicine."`'
        )

    if x == 75:

        await event.eor(
            '`"Night before a day off is more satisfying than the actual day off."`'
        )

    if x == 76:

        await event.eor('`"We put paper in a folder to keep it from folding."`')

    if x == 77:

        await event.eor(
            '`"Somewhere, two best friends are meeting for the first time."`'
        )

    if x == 78:

        await event.eor(
            '`"Our brain simultaneously hates us, loves us, doesn\'t care about us, and micromanages our every move."`'
        )

    if x == 79:

        await event.eor(
            '`"Being a male is a matter of birth. Being a man is a matter of age. But being a gentleman is a matter of choice."`'
        )

    if x == 80:

        await event.eor(
            '`"Soon the parents will be hiding their social account from their kids rather than kids hiding their accounts from the parents."`'
        )

    if x == 81:

        await event.eor('`"Wikipedia is what the internet was meant to be."`')

    if x == 82:

        await event.eor(
            '`"A theme park is the only place that you can hear screams in the distance and not be concerned."`'
        )

    if x == 83:

        await event.eor(
            '`"A wireless phone charger offers less freedom of movement than a wired one."`'
        )

    if x == 84:

        await event.eor(
            "`\"If you repeatedly criticize someone for liking something you don't, they won't stop liking it. They'll stop liking you.\"`"
        )

    if x == 85:

        await event.eor(
            '`"Somewhere there is a grandmother, whose grandson really is the most handsome boy in the world."`'
        )

    if x == 86:

        await event.eor(
            '`"If someday human teleportation becomes real, people will still be late for work."`'
        )

    if x == 87:

        await event.eor(
            '`"The first humans who ate crabs must have been really hungry to try and eat an armored sea spider"`'
        )

    if x == 88:

        await event.eor(
            '`"Doing something alone is kind of sad, but doing it solo is cool af."`'
        )

    if x == 89:

        await event.eor(
            '`"Your brain suddenly becomes perfect at proofreading after you post something."`'
        )

    if x == 90:

        await event.eor(
            '`"There\'s always that one song in your playlist that you always skip but never remove."`'
        )

    if x == 91:

        await event.eor(
            '`"Kids next century will probably hate us for taking all the good usernames."`'
        )

    if x == 92:

        await event.eor('`"Bubbles are to fish what rain is to humans."`')

    if x == 93:

        await event.eor(
            '`"The more people you meet, the more you realise and appreciate how well your parents raised you."`'
        )

    if x == 94:

        await event.eor('`"A comma is a short pause, a coma is a long pause."`')

    if x == 95:

        await event.eor('`"Someday you will either not wake up or not go to sleep."`')

    if x == 96:

        await event.eor(
            '`"Bermuda Triangle might be the exit portal of this simulation."`'
        )

    if x == 97:

        await event.eor(
            '`"If we put solar panels above parking lots, then our cars wouldn\'t get hot and we would have a lot of clean energy."`'
        )
