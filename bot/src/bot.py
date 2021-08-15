import os
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv("../resources/.env")
token = os.getenv("DISCORD_TOKEN")
name = os.getenv("BOT_NAME")

client = commands.Bot(command_prefix='!')

is_active = False
skip_first = True
reminder_toggle = False
reminder_minutes = 30


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
    try:
        arg = int(arg)
    except ValueError:
        pass

    if isinstance(arg, int) and arg > 0:
        remind_user.change_interval(minutes=arg)
        await ctx.send(f"Ok I'm going to remind you every {arg} minutes.")
    else:
        await ctx.send("I'm sorry but you didn't provide a proper time argument.")


@client.command()
async def info(ctx):
    await ctx.send(
        f"Hi my name is {name}. I'm here to help you while you're working on your computer. Once you turn me"
        f" on I'm going to remind you every {reminder_minutes} minutes, or you can also tell me another "
        f"time, to either drink or stretch. This should help you to stay relaxed and healthy and thus "
        f"improve your productivity and well-being. I'm always happy to hear from you! :)"
        )


@tasks.loop(minutes=reminder_minutes)
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
