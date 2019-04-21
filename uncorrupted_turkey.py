import json
import random

from discord import Game, Status
from discord.ext.commands import Bot

BOT_PREFIX = ('!', '?')
TOKEN = 'NTY5MTY3NzAyNDM4OTY5Mzg0.XLsvXQ.riryPznr8KknKGWv9CG8lNg2syQ'
items = {}


def bold(s):
    return '**' + s + '**'


def italics(s):
    return '*' + s + '*'


def load_items():
    items = {}
    with open('data/items.json', 'r') as f:
        data = json.load(f)
        for item in data['items']:
            items[item['name']] = item
    print("{} items loaded from file".format(len(items)))
    return items


client = Bot(command_prefix=BOT_PREFIX, status=Status.online, activity=Game("New World"))


@client.event
async def on_ready():
    global items
    items = load_items()
    print("Logged in as " + client.user.name)


@client.event
async def on_disconnect():
    await client.change_presence(afk=True)
    print("Disconnect")


@client.event
async def on_error(event_method, *args, **kwargs):
    await client.change_presence(afk=True)
    print("Error")


@client.command(description="Welcome message", brief="Welcome message")
async def welcome(ctx):
    await ctx.send(":turkey: *Signals friendly intentions*\nGreetings @everyone! I am the all-knowing Uncorrupted Turkey. Type '!help item' to see how I can assist you with crafting.")


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
        await message.channel.send(':turkey: {}'.format(random.choice(sentences)))
    elif 'tukey' in message.content:
        await message.channel.send(":turkey: :disappointed: Hey! It is spelled 'turkey'.")
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
        "I have 86.7% corruption resistance."
    ]
    await ctx.send(":turkey: Hello {}! {}".format(str(ctx.message.author)[:str(ctx.message.author).find('#')], random.choice(tips)))


@client.command(description="Describes the queried item, e.g. try '!item steel ingot'. Try to use the item name exactly as written in the game (later I'll be able to make best-guess estimates). For now, I only know about items in the 'Refining' and 'Blacksmithing' categories. Will know more soon.",
                brief='Describe the queried item')
async def item(ctx, *args):
    global items
    message = []
    item_name = ' '.join(args).lower()
    if item_name == 'turkey':
        await ctx.send(":angry: A turkey is not an item, we are the original inhabitants of this island.")
        return
    if item_name not in items:
        await ctx.send("I don't know the item: {}. Try to write the name exactly as you see it in game (not case sensitive). You may also have to specify the full material qualifiers, e.g. 'leather' won't work, but 'rugged leather' will. Note that I only know about items in the Refining and Blacksmithing categories right now.".format(italics(item_name)))
        return
    message.append(bold('Item') + ': ' + italics(item_name))
    item = items[item_name]

    # tier
    if 'tier' in item:
        message.append("{}: {}".format(bold('Tier'), item['tier']))

    # skill required
    if 'skill' in item:
        message.append("{}: {}  LEVEL {}".format(bold('Skill required'), italics(item['skill']['name']), item['skill']['level']))

    # ingredients
    if 'ingredients' in item and item['ingredients']:
        message.append(bold('Ingredients') + ':')
        for ingredient in item["ingredients"]:
            message.append("• {}, {}".format(italics(ingredient['name']) ,ingredient['quantity']))
    else:
        message.append('This is a raw item with no ingredients.')
    await ctx.send('\n'.join(message))

client.run(TOKEN)
