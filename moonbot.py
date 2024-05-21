import os
import random
import discord
from discord.ext import commands
from discord import option
from eclipse_parsing import fileToList, parseEclipseFile, parseEclipse

# Eclipse Data Source: https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html

heroku = False  # set to true if hosting on heroku

if heroku == True:
    BOT_TOKEN = os.environ['BOT_TOKEN']
else:
    from dotenv import load_dotenv
    load_dotenv('BOT_TOKEN.env')
    BOT_TOKEN = os.getenv('BOT_TOKEN')

# add discord application commands
bot = commands.Bot()

def randomIndex(listName):
    """Returns a random element within a given list"""
    index = random.randint(0, len(listName)-1)
    content = listName[index].strip('\n')
    return content

moonfacts = list(set(fileToList("moonfacts.txt")))
moonimgs = list(set(fileToList("moonimgs.txt")))
moonvideos = list(set(fileToList("moonvideos.txt")))
eclipseData = parseEclipseFile(fileToList("future_eclipses.txt"))

moonmedia = moonimgs + moonvideos
random.shuffle(moonmedia)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/moon-help ⁺₊☾☁︎'))
    print(f'Logged in as {bot.user}')
               
@bot.slash_command(name="moon-fact", description="Send a random moon fact, with optional keyword.")
@option("keyword", str, description="This word will be present in the provided fact.")
async def moon_fact(ctx, keyword: str):
    # Filter moonfacts based on the provided keyword
    filtered_facts = []
    if keyword:
        filtered_facts = [fact for fact in moonfacts if keyword.lower() in fact.lower()]
    if not keyword or not filtered_facts:
        filtered_facts = moonfacts

    random_fact = random.choice(filtered_facts)
    embed = discord.Embed(title="Moon Fact!", color=0x36393e)
    if keyword and (filtered_facts == moonfacts):
        no_kword = f"Unfortunately, no moon facts were found containing the provided keyword '{keyword}'.\n\n⁺₊ Have a random moon fact anyway! ⁺₊"
        embed.add_field(name=no_kword, value=random_fact, inline=False)
    else:
        embed.add_field(name="⁺₊ Did you know? ⁺₊", value=random_fact, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="moon-image", description="Send a random moon image.")
async def moon_picture(ctx):
    url = randomIndex(moonimgs)
    if ".gif" not in url:
        if "https://media.discordapp.net/attachments/" in url:
            embed = discord.Embed(title="⁺₊ Moon Image ⁺₊", description="Taken by Dennis Melka", color=0x36393e)
        else:
            embed = discord.Embed(title="⁺₊ Moon Image ⁺₊", color=0x36393e)
        embed.set_image(url=url)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(url)
    
@bot.slash_command(name="moon-media", description="Send random moon media.")
async def moon_media(ctx):
    url = randomIndex(moonmedia)
    await ctx.respond(url)

@bot.slash_command(name="moon-video", description="Send a random moon video.")
async def moon_video(ctx):
    url = randomIndex(moonvideos)
    await ctx.respond(url)
    
@bot.slash_command(name="next-eclipse", description="Receive information about the next solar eclipse, optionally specifying region, type, or year.")
@option("keyword", str, description="Provide a specific region, eclipse type, or year.")
async def next_eclipse(ctx, keyword: str = None):
    if keyword:
        if keyword.isnumeric():
            specifier = "year"
        elif keyword.lower() == "partial" or keyword.lower() == "annular" or keyword.lower() == "total":
            specifier = "type"
        else:
            specifier = "region"
        
    target_eclipse = None
    if keyword and specifier == "year":
        for eclipse in eclipseData:
            if len(keyword) == 4 and keyword in eclipse['date'].lower():
                target_eclipse = eclipse
                break
    elif keyword and specifier == "type":
        for eclipse in eclipseData:
            if keyword.lower() == eclipse['eclipse_type'].lower():
                target_eclipse = eclipse
                break
    elif keyword and specifier == "region":
        for eclipse in eclipseData:
            if len(keyword) > 3 and keyword.lower() in eclipse['geographic_region'].lower():
                target_eclipse = eclipse
                break
    if not keyword:
        target_eclipse = eclipseData[0]

    embed = discord.Embed(title="Upcoming Solar Eclipse...", color=0x36393e)

    if keyword and not target_eclipse:
        no_kword = f"No upcoming eclipse was found with the given criteria '{keyword}'. Note that eclipse data is loaded up to the year 2100, and country abbreviations should be seperated by periods (ex. U.S., N.Z.). \n\nHere is information about the soonest solar eclipse:"
        eclipse_str = parseEclipse(eclipseData[0])
        embed.add_field(
            name=no_kword,
            value=f"* The {eclipse_str[0]}{eclipse_str[1]}\n[Source: NASA](https://eclipse.gsfc.nasa.gov/solar.html)",
            inline=False
        )
    else:
        eclipse_str = parseEclipse(target_eclipse)
        if keyword and specifier == "region":
            embed.add_field(
                name=f"In {keyword}, the soonest {eclipse_str[0]}",
                value=f"\n{eclipse_str[1]}\n[Source: NASA](https://eclipse.gsfc.nasa.gov/solar.html)",
                inline=False
            )
        elif keyword and specifier == "year":
            embed.add_field(
                name=f"In {keyword}, the first {eclipse_str[0]}",
                value=f"\n{eclipse_str[1]}\n[Source: NASA](https://eclipse.gsfc.nasa.gov/solar.html)",
                inline=False
            )
        elif keyword and specifier == "type":
            embed.add_field(
                name=f"The {eclipse_str[0]}",
                value=f"\n{eclipse_str[1]}\n[Source: NASA](https://eclipse.gsfc.nasa.gov/solar.html)",
                inline=False
            )
        else:
            embed.add_field(
                name=f"The {eclipse_str[0]}",
                value=f"\n{eclipse_str[1]}\n[Source: NASA](https://eclipse.gsfc.nasa.gov/solar.html)",
                inline=False
            )
    await ctx.respond(embed=embed)
        
@bot.slash_command(name="moon-help", description="moonbot help")
async def help_command(ctx):
    embed = discord.Embed(title="☁︎☾☁︎ Moon Bot Commands ☁︎☾☁︎", color=0x36393e)
    embed.add_field(name="/moon-fact", value="Send a random moon fact, with optional keyword.", inline=False)
    embed.add_field(name="/moon-media", value="Send random moon media.", inline=False)
    embed.add_field(name="/moon-image", value="Send a random moon image.", inline=False)
    embed.add_field(name="/moon-video", value="Send a random moon video.", inline=False)
    embed.add_field(name="/next-eclipse", value="Receive information about the next solar eclipse, optionally in a specified region.", inline=False)
    await ctx.respond(embed=embed)

bot.run(BOT_TOKEN)