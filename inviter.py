import discord
import os
import config
import logging
import aiohttp
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True



client = commands.AutoShardedBot(intents=intents,command_prefix=['>>'],case_insensitive=True)
client.version = "v1.0.0"

@client.event
async def on_ready():
 print("Logged in as" , client.user)
    
logging.basicConfig(level=logging.WARNING)


for filename in os.listdir('./cogs'): #search in cogs folder, make sure its named cogs and is in same directory as of the main file
     if filename.endswith(".py"): #This makes bot ignore  other files.(Eg:- .txt,.png)
            client.load_extension(f'cogs.{filename[:-3]}') #this is where the bot loads the extension

client.run(config.token)
