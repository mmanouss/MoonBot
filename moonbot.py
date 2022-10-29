import os
import discord
import random
from dotenv import load_dotenv

load_dotenv('BOT_TOKEN.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client() 

def fileToList(fileName: str) -> list:
    """Converts a given file into a list"""
    fileNamefile = open(fileName, "r")
    fileList = fileNamefile.readlines()
    return fileList

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

client.run(BOT_TOKEN)
