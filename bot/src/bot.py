import os
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv("../resources/.env")
token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix='!')

is_active = False
skip_first = True
reminder_toggle = False
reminder_minutes = 10


@client.event
async def on_ready():
    print("\033[92mLOG: bot is up and ready\033[0m")
    
    
@client.command()
async def on(ctx):
    global is_active

    if is_active:
        await ctx.send("Keep calm! I'm already active")
    else:
        remind_user.start(ctx)
        is_active = True
        await ctx.send("I'm active now!")
    

@client.command()
async def off(ctx):
    global is_active
    global skip_first

    if is_active:
        skip_first = True
        remind_user.stop()
        is_active = False
        await ctx.send("I'm going to sleep now. See you!")
    else:
        await ctx.send("Don't disturb me while I'm sleeping!")
    

@client.command()
async def set_time(ctx, arg):
    # TODO in #12
    pass


@client.command()
async def info(ctx):
    # TODO in #9
    pass


@tasks.loop(seconds=reminder_minutes)
async def remind_user(ctx):
    global reminder_toggle
    global skip_first

    if skip_first:
        skip_first = False
        return

    if reminder_toggle:
        await send_hydrate_reminder(ctx)
    else:
        await send_stretch_reminder(ctx)

    reminder_toggle = not reminder_toggle


async def send_hydrate_reminder(ctx):
    await ctx.send("Do you feel like you need to hydrate?")


async def send_stretch_reminder(ctx):
    await ctx.send("It's time to stretch now!")


client.run(token)
