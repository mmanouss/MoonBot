import os
import discord
from dotenv import load_dotenv

load_dotenv('BOT_TOKEN.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client() 

@client.event
async def on_ready():
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.listening, name='moon enjoyers :)'))
    print(f'Logged in as {client.user}') 
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(BOT_TOKEN)
