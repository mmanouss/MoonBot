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
bot = commands.Bot(command_prefix="")

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

confused_moon_responses = ["Are you talking to me?",
                           "Am I supposed to respond to that :,)",
                           "I don't know what you want me to do..."]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='moon enjoyers :)'))
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
         return
    if message.content[:5] == "moon-" and len(message.content) > 5:
        await bot.process_commands(message)
    else:
        if ('moon' in message.content.lower() and 'fact' in message.content.lower()):
            await message.add_reaction(emoji=str('🌚'))
            await message.channel.send('Did you know?\n'+randomIndex(moonfacts)+'!')
        elif ('moon' in message.content.lower() and 'picture' in message.content.lower()) or ('moon' in message.content.lower() and 'image' in message.content.lower()):
            await message.add_reaction(emoji=str('🌚'))
            await message.channel.send(randomIndex(moonimgs))
        elif 'moon' in message.content.lower() and 'gif' in message.content.lower():
            await message.add_reaction(emoji=str('🌚'))
            await message.channel.send(randomIndex(moongifs))
        elif ('moon' in message.content.lower() and 'video' in message.content.lower()) or ('moon' in message.content.lower() and 'movie' in message.content.lower()):
            await message.add_reaction(emoji=str('🌚'))
            await message.channel.send(randomIndex(moonvideos))
        elif 'moon' in message.content.lower():
            await message.add_reaction(emoji=str('🌜'))
            contentType = random.randint(0, 3)
            if contentType == 0 or contentType == 1 or contentType == 2:
                await message.channel.send('Did you know?\n'+randomIndex(moonfacts)+'!')
            elif contentType == 3:
                await message.channel.send(randomIndex(moonmedia))
            
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction(emoji=str('❔'))
        await ctx.send(random.choice(confused_moon_responses))
             
@bot.command(name="moon-fact", description="Send a random moon fact.")
async def moon_fact(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send('Did you know?\n' + randomIndex(moonfacts) + '!')

@bot.command(name="moon-image", description="Send a random moon image.")
async def moon_picture(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send(randomIndex(moonimgs))

@bot.command(name="moon-gif", description="Send a random moon gif.")
async def moon_gif(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send(randomIndex(moongifs))

@bot.command(name="moon-video", description="Send a random moon video.")
async def moon_video(ctx):
    await ctx.message.add_reaction(emoji='🌚')
    await ctx.send(randomIndex(moonvideos))
        
@bot.command(name="moon-help", description="moonbot help")
async def help_command(ctx):
    embed = discord.Embed(title="Moon Bot Commands", color=0x36393e)
    embed.add_field(name="moon-fact", value="Send a random moon fact.", inline=False)
    embed.add_field(name="moon-image", value="Send a random moon image.", inline=False)
    embed.add_field(name="moon-gif", value="Send a random moon gif.", inline=False)
    embed.add_field(name="moon-video", value="Send a random moon video.", inline=False)
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
