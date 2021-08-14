import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("../resources/.env")
token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print("\033[92mLOG: bot is up and ready\033[0m")

client.run(token)
