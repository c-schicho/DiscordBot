import os
import random
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
from resources.messages import *

load_dotenv("resources/.env")

TOKEN = os.getenv("DISCORD_TOKEN")
NAME = os.getenv("BOT_NAME")
REMINDER_MINUTES = int(os.getenv("REMINDER_MINUTES"))

is_active = False
skip_first = True
reminder_toggle = False

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(Log.ready)
    
    
@client.command()
async def on(ctx):
    global is_active

    if is_active:
        await ctx.send(On.already_active)
    else:
        remind_user.start(ctx)
        is_active = True
        await ctx.send(On.active)
    

@client.command()
async def off(ctx):
    global is_active
    global skip_first

    if is_active:
        skip_first = True
        remind_user.stop()
        is_active = False
        await ctx.send(Off.inactive)
    else:
        await ctx.send(Off.already_inactive)
    

@client.command()
async def set_time(ctx, arg):
    try:
        arg = int(arg)
    except ValueError:
        pass

    if isinstance(arg, int) and arg > 0:
        remind_user.change_interval(minutes=arg)
        await ctx.send(SetTime().success(arg))
    else:
        await ctx.send(SetTime.failure)


@client.command()
async def info(ctx):
    await ctx.send(Information().message(NAME, REMINDER_MINUTES))


@tasks.loop(minutes=REMINDER_MINUTES)
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
    messages = [
        HydrationMessages.message01,
        HydrationMessages.message02,
        HydrationMessages.message03,
        HydrationMessages.message04,
        HydrationMessages.message05
    ]
    await ctx.send(random.choice(messages))


async def send_stretch_reminder(ctx):
    messages = [
        StretchMessages.message01,
        StretchMessages.message02,
        StretchMessages.message03,
        StretchMessages.message04,
        StretchMessages.message05
    ]
    await ctx.send(random.choice(messages))


client.run(TOKEN)
