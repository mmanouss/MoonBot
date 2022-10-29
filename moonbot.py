import os
import discord
import random

heroku = False #set to true if hosting on heroku

if heroku == True:
    BOT_TOKEN = os.environ['BOT_TOKEN']
else:
    from dotenv import load_dotenv
    load_dotenv('BOT_TOKEN.env')
    BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client() 

def fileToList(fileName: str) -> list:
    """Converts a given file into a list"""
    fileNamefile = open(fileName, "r")
    fileList = fileNamefile.readlines()
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
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.listening, name='moon enjoyers :)'))
    print(f'Logged in as {client.user}') 
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif ('moon' in message.content.lower() and 'fact' in message.content.lower()):
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

client.run(BOT_TOKEN)
