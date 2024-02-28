import os
import discord
from discord.ext import commands
import random

heroku = False  # set to true if hosting on heroku

if heroku == True:
    BOT_TOKEN = os.environ['BOT_TOKEN']
else:
    from dotenv import load_dotenv
    load_dotenv('BOT_TOKEN.env')
    BOT_TOKEN = os.getenv('BOT_TOKEN')

# add discord application commands
intents = discord.Intents.default()
intents.messages = True
client = commands.Bot(command_prefix='', intents=intents)

def fileToList(fileName: str) -> list:
    """Converts a given file into a list"""
    with open(fileName, "r") as file:
        fileList = file.readlines()
    return fileList

def randomIndex(listName):
    """Returns a random element within a given list"""
    index = random.randint(0, len(listName)-1)
    content = listName[index].strip('\n')
    return content

moonfacts = fileToList("moonfacts.txt")
moonimgs = fileToList("moonimgs.txt")
moongifs = fileToList("moongifs.txt")
moonvideos = fileToList("moonvideos.txt")

moonmedia = moonimgs + moongifs + moonvideos
random.shuffle(moonmedia)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='moon enjoyers :)'))
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command(name='moon-fact')
async def moon_fact(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send('Did you know?\n' + randomIndex(moonfacts) + '!')

@client.command(name='moon-picture')
async def moon_picture(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send(randomIndex(moonimgs))

@client.command(name='moon-gif')
async def moon_gif(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send(randomIndex(moongifs))

@client.command(name='moon-video')
async def moon_video(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send(randomIndex(moonvideos))

@client.command(name='moon')
async def moon(ctx):
    await ctx.message.add_reaction(emoji='🌜')
    content_type = random.randint(0, 3)
    # make facts a more common outcome than media
    if content_type in [0, 1, 2]:
        await ctx.send('Did you know?\n' + randomIndex(moonfacts) + '!')
    elif content_type == 3:
        await ctx.send(randomIndex(moonmedia))
        
@client.command(name='moon-help')
async def help_command(ctx):
    embed = discord.Embed(title="Moon Bot Commands", color=0x36393e)
    embed.add_field(name="moon-fact", value="Send a random moon fact.", inline=False)
    embed.add_field(name="moon-picture", value="Send a random moon picture.", inline=False)
    embed.add_field(name="moon-gif", value="Send a random moon gif.", inline=False)
    embed.add_field(name="moon-video", value="Send a random moon video.", inline=False)
    embed.add_field(name="moon", value="Send a moon fact or random moon media.", inline=False)
    await ctx.send(embed=embed)

client.run(BOT_TOKEN)
