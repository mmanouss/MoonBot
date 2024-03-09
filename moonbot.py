import os
import random
import discord
from discord.ext import commands

heroku = False  # set to true if hosting on heroku

if heroku == True:
    BOT_TOKEN = os.environ['BOT_TOKEN']
else:
    from dotenv import load_dotenv
    load_dotenv('BOT_TOKEN.env')
    BOT_TOKEN = os.getenv('BOT_TOKEN')

# add discord application commands
bot = commands.Bot()

def fileToList(fileName: str) -> list:
    """Converts a given file into a list"""
    with open(fileName, "r") as file:
        fileList = file.readlines()
    return list(set(fileList))

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

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/moon-help ⁺₊☾☁︎'))
    print(f'Logged in as {bot.user}')
               
@bot.slash_command(name="moon-fact", description="Send a random moon fact, with optional keyword.")
async def moon_fact(ctx, keyword: str = None):
    # Filter moonfacts based on the provided keyword
    filtered_facts = []
    if keyword:
        filtered_facts = [fact for fact in moonfacts if keyword.lower() in fact.lower()]
    if not keyword or not filtered_facts:
        filtered_facts = moonfacts

    random_fact = random.choice(filtered_facts)
    embed = discord.Embed(title="Moon Fact!", color=0x36393e)
    if keyword and (filtered_facts == moonfacts):
        no_kword = "Unfortunately, no moon facts were found containing the provided keyword '" + keyword + "'.\n\n" + "⁺₊ Have a random moon fact anyway! ⁺₊"
        embed.add_field(name=no_kword, value=random_fact, inline=False)
    else:
        embed.add_field(name="⁺₊ Did you know? ⁺₊", value=random_fact, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="moon-image", description="Send a random moon image.")
async def moon_picture(ctx):
    embed = discord.Embed(title="⁺₊ Moon Image ⁺₊", color=0x36393e)
    url = randomIndex(moonimgs)
    embed.set_image(url=url)
    await ctx.respond(embed=embed)
    
@bot.slash_command(name="moon-media", description="Send random moon media.")
async def moon_media(ctx):
    url = randomIndex(moonmedia)
    await ctx.respond(url)

@bot.slash_command(name="moon-gif", description="Send a random moon gif.")
async def moon_gif(ctx):
    url = randomIndex(moongifs)
    await ctx.respond(url)

@bot.slash_command(name="moon-video", description="Send a random moon video.")
async def moon_video(ctx):
    url = randomIndex(moonvideos)
    await ctx.respond(url)
        
@bot.slash_command(name="moon-help", description="moonbot help")
async def help_command(ctx):
    embed = discord.Embed(title="☁︎☾☁︎ Moon Bot Commands ☁︎☾☁︎", color=0x36393e)
    embed.add_field(name="/moon-fact", value="Send a random moon fact, with optional keyword.", inline=False)
    embed.add_field(name="/moon-media", value="Send random moon media.", inline=False)
    embed.add_field(name="/moon-image", value="Send a random moon image.", inline=False)
    embed.add_field(name="/moon-gif", value="Send a random moon gif.", inline=False)
    embed.add_field(name="/moon-video", value="Send a random moon video.", inline=False)
    await ctx.respond(embed=embed)

bot.run(BOT_TOKEN)
