import os
import random
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import resources.messages as Msg

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
    print(Msg.Log.ready)
    
    
@client.command(
    help="This command activates the reminder functionality of the bot. "
         "It will then send you messages in the defined intervals.",
    brief="Activates the bot"
)
async def on(ctx):
    global is_active

    if is_active:
        await ctx.send(Msg.On.already_active)
    else:
        remind_user.start(ctx)
        is_active = True
        await ctx.send(Msg.On.active)
    

@client.command(
    help="This command deactivates the reminder functionality of the bot. "
         "It will then stop to send you reminder messages.",
    brief="Deactivates the bot"
)
async def off(ctx):
    global is_active
    global skip_first

    if is_active:
        skip_first = True
        remind_user.stop()
        is_active = False
        await ctx.send(Msg.Off.inactive)
    else:
        await ctx.send(Msg.Off.already_inactive)
    

@client.command(
    help="Sets a custom remind time. Provide the time for the desired remind interval in minutes after the command.",
    brief="Sets a custom remind time"
)
async def set_time(ctx, arg):
    try:
        arg = int(arg)
    except ValueError:
        pass

    if isinstance(arg, int) and arg > 0:
        remind_user.change_interval(minutes=arg)
        await ctx.send(Msg.SetTime().success(arg))
    else:
        await ctx.send(Msg.SetTime.failure)


@client.command(
    help="This command will provide you further information about the bot, mainly what it is supposed to do.",
    brief="Provides further information about the bot"
)
async def info(ctx):
    await ctx.send(Msg.Information().message(NAME, REMINDER_MINUTES))


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
        Msg.HydrationMessages.message01,
        Msg.HydrationMessages.message02,
        Msg.HydrationMessages.message03,
        Msg.HydrationMessages.message04,
        Msg.HydrationMessages.message05
    ]
    await ctx.send(random.choice(messages))


async def send_stretch_reminder(ctx):
    messages = [
        Msg.StretchMessages.message01,
        Msg.StretchMessages.message02,
        Msg.StretchMessages.message03,
        Msg.StretchMessages.message04,
        Msg.StretchMessages.message05
    ]
    await ctx.send(random.choice(messages))


client.run(TOKEN)
