import random

from discord import Game, Status
from discord.ext.commands import Bot
from common.discord_formatting import *
from common.items import load_items, get_item


BOT_PREFIX = ('!', '?')
TOKEN = 'NTY5MTY3NzAyNDM4OTY5Mzg0.XLsvXQ.riryPznr8KknKGWv9CG8lNg2syQ'
ITEMS = load_items()

client = Bot(command_prefix=BOT_PREFIX, status=Status.online, activity=Game("New World"))


# EVENTS
@client.event
async def on_ready():
    print("Logged in as " + client.user.name)


@client.event
async def on_disconnect():
    await client.change_presence(afk=True)
    print("Disconnect")


@client.event
async def on_error(event_method, *args, **kwargs):
    await client.change_presence(afk=True)
    print("Error")


# COMMANDS
@client.command(description="for dev use", brief="for dev use")
async def debug(ctx):
    pass


@client.command(description="unstuck", brief="unstuck")
async def unstuck(ctx):
    await ctx.send("Huh?")


@client.event
async def on_message(message):
    sentences = [
        "Did somebody say turkey?",
        "My ears are burning.",
        "Ahem, I'm right here..."
    ]
    if message.author.bot:
        return
    if 'turkey' in message.content:
        await message.channel.send(turkey_message(random.choice(sentences)))
    elif 'tukey' in message.content:
        await message.channel.send(turkey_message(":disappointed: Hey! It is spelled 'turkey'."))
    await client.process_commands(message)


@client.command(description="Say Hello", brief="Say Hello")
async def hello(ctx):
    tips = [
        "Watch out for Omni.",
        "Don't harm the turkeys.",
        "There is a secret elk level.",
        "Happy hunting.",
        "We need more Wyrdwood.",
        "My feathers are Exquisite.",
        "Drink plenty of fluids.",
        "I have 86.7% corruption resistance.",
        "Gobble Gobble."
    ]
    await ctx.send(":turkey: *Signals friendly intentions*\nHello {}! I am the all-knowing Uncorrupted Turkey. Type '!help item' to see how I can assist you with crafting. \n{}".format(str(ctx.message.author)[:str(ctx.message.author).find('#')], random.choice(tips)))


@client.command(description="Describes the queried item, e.g. try '!item steel ingot'. For now, I only know about items in the 'Refining' and 'Blacksmithing' categories. Will know more soon.",
                brief='Describe the queried item')
async def item(ctx, *args):
    THRESH = 30  # if query is more than THRESH from any known items, it's probably not one we know
    message = []
    item_name = ' '.join(args).lower().strip()
    print("Querying item: " + item_name)
    if not item_name:
        return
    if item_name == 'turkey':
        await ctx.send(turkey_message(":angry: A turkey is not an item, we are the original inhabitants of this island."))
        return
    if item_name not in ITEMS:
        best_guess, distance = get_item(item_name, ITEMS)
        print("'{}' '{}' distance: {}".format(item_name, best_guess, distance))
        if distance > THRESH:
            await ctx.send(turkey_message("I don't know the item: {}. Try to write the name as you see it in game (not case sensitive). Note that I only know about items in the Refining and Blacksmithing categories right now.".format(italics(item_name))))
            return
        else:
            message.append(turkey_message("I don't know the item: {}. I'm going to go out on a turkey leg and guess you meant the item: {}?".format(italics(item_name), italics(best_guess))))
            item_name = best_guess

    item = ITEMS[item_name]
    message.append(bold('Item') + ': ' + italics(item_name))

    # tier
    if 'tier' in item:
        message.append("{}: {}".format(bold('Tier'), item['tier']))

    # skill required
    if 'skill' in item:
        message.append("{}: {}  LEVEL {}".format(bold('Skill required'), italics(item['skill']['name']), item['skill']['level']))

    # attr required
    # TODO attr required

    # ingredients
    if 'ingredients' in item and item['ingredients']:
        message.append(bold('Ingredients') + ':')
        for ingredient in item["ingredients"]:
            message.append("• {}, {}".format(italics(ingredient['name']) ,ingredient['quantity']))
    else:
        message.append('This is a raw item with no ingredients.')

    await ctx.send('\n'.join(message))

client.run(TOKEN)
