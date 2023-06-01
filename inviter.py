import discord
import os
import config
import logging
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True


client = commands.AutoShardedBot(
    intents=intents, command_prefix=[">>"], case_insensitive=True
)
client.version = "v1.2.0"


@client.event
async def on_ready():
    print("Logged in as", client.user)


logging.basicConfig(level=logging.WARNING)


async def main():
    async with client:
        for filename in os.listdir(
            "./cogs"
        ):  # search in cogs folder, make sure its named cogs and is in same directory as of the main file
            if filename.endswith(
                ".py"
            ):  # This makes bot ignore  other files.(Eg:- .txt,.png)
                await client.load_extension(
                    f"cogs.{filename[:-3]}"
                )  # this is where the bot loads the extension
        await client.start(config.token)


asyncio.run(main())
