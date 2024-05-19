import os
import random
import discord
from discord.ext import commands
from eclipse_parsing import parseEclipseData

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

def fileToList(fileName: str) -> list:
    """Converts a given file into a list"""
    with open(fileName, "r") as file:
        return file.readlines()

def randomIndex(listName):
    """Returns a random element within a given list"""
    index = random.randint(0, len(listName)-1)
    content = listName[index].strip('\n')
    return content

moonfacts = list(set(fileToList("moonfacts.txt")))
moonimgs = list(set(fileToList("moonimgs.txt")))
moonvideos = list(set(fileToList("moonvideos.txt")))
eclipseData = parseEclipseData(fileToList("future_eclipses.txt"))

moonmedia = moonimgs + moonvideos
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
    
@bot.slash_command(name="next-eclipse", description="Receive a countdown to the next total solar eclipse date and location(s).")
async def next_eclipse(ctx, keyword: str = None):
    if keyword:
        next_eclipse = None
        for eclipse in eclipseData:
            if keyword.lower() in eclipse['geographic_region'].lower():
                next_eclipse = eclipse
                break
    else:
        next_eclipse = eclipseData[0]
    
    eclipse_magnitude_info = ". The eclipse magnitude represents how much of the Sun's diameter is obscured by the Moon during the peak of an eclipse."
    eclipse_magnitude_calculation = f"The moon's apparent diameter will be {next_eclipse['eclipse_magnitude']*100}% of the Sun's apparent diameter, so "
    eclipse_magnitude_specifics = {"Total": eclipse_magnitude_calculation + "the Sun will be completely covered. ", 
                                "Partial": eclipse_magnitude_calculation + "a portion of the Sun will be visible. ", 
                                "Annular": eclipse_magnitude_calculation + "the outer edge of the Sun will still be visible. "}
    
    eclipse_info = f"The next solar eclipse will be {next_eclipse['eclipse_type']} on {next_eclipse['date']} at {next_eclipse['time_of_greatest_eclipse']} UTC, with a central duration of {next_eclipse['central_duration']}" + eclipse_magnitude_info + eclipse_magnitude_specifics[next_eclipse['eclipse_type']] + f"It will be visible in {next_eclipse['geographic_region']}."
    
    # Eclipse countdown logic
    import datetime
    eclipse_datetime = datetime.datetime.strptime(next_eclipse["date"] + " " + next_eclipse["time_of_greatest_eclipse"], "%Y %b %d %H:%M:%S")
    time_remaining = eclipse_datetime - datetime.datetime.now(datetime.UTC)
    days_remaining = time_remaining.days
    hours_remaining, remainder = divmod(time_remaining.seconds, 3600)
    minutes_remaining, seconds_remaining = divmod(remainder, 60)
    countdown = f"The eclipse will occur in {days_remaining} days, {hours_remaining} hours, {minutes_remaining} minutes, and {seconds_remaining} seconds."
    
    embed = discord.Embed(title="Upcoming Solar Eclipse...", color=0x36393e)
    if keyword and not next_eclipse:
        no_kword = f"Unfortunately, no eclipse was found in the given region of '{keyword}'.\n\nHere is information about the upcoming solar eclipse:"
        embed.add_field(name=no_kword, value=eclipse_info + "\n\n" + countdown, inline=False)
    else:
        embed.add_field(name="Solar Eclipse: "+next_eclipse["date"], value=eclipse_info + "\n\n" + countdown, inline=False)
    await ctx.respond(embed=embed)
        
@bot.slash_command(name="moon-help", description="moonbot help")
async def help_command(ctx):
    embed = discord.Embed(title="☁︎☾☁︎ Moon Bot Commands ☁︎☾☁︎", color=0x36393e)
    embed.add_field(name="/moon-fact", value="Send a random moon fact, with optional keyword.", inline=False)
    embed.add_field(name="/moon-media", value="Send random moon media.", inline=False)
    embed.add_field(name="/moon-image", value="Send a random moon image.", inline=False)
    embed.add_field(name="/moon-video", value="Send a random moon video.", inline=False)
    embed.add_field(name="/next-eclipse", value="Receive a countdown to the next total solar eclipse date and location(s).", inline=False)
    await ctx.respond(embed=embed)

bot.run(BOT_TOKEN)
