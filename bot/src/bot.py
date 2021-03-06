import os
import random
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import resources.messages as Msg
from tinydb import TinyDB, Query

db = TinyDB("resources/user_db.json", sort_keys=True, indent=4, separators=(',', ': '))
db.default_table_name = "user_settings"
load_dotenv("resources/.env")

TOKEN = os.getenv("DISCORD_TOKEN")
NAME = os.getenv("BOT_NAME")
REMINDER_MINUTES = int(os.getenv("REMINDER_MINUTES"))

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    db.update({"is_active": False, "skip_first": True})
    print(Msg.Log.ready)


@client.command(
    help="This command activates the reminder functionality of the bot. "
         "It will then send you messages in the defined intervals.",
    brief="Activates the bot"
)
async def on(ctx):
    usr, usr_id, usr_settings = _get_user_and_settings(ctx)
    is_active = usr_settings["is_active"]
    reminder_minutes = usr_settings["reminder_minutes"]

    if is_active:
        await ctx.send(Msg.On.already_active)
    else:
        try:
            remind_user.change_interval(minutes=reminder_minutes)
            remind_user.start(ctx)
            db.update({"is_active": True}, usr.id == usr_id)
            await ctx.send(Msg.On.active)
        except RuntimeError:
            await ctx.send(Msg.On.failure)


@client.command(
    help="This command deactivates the reminder functionality of the bot. "
         "It will then stop to send you reminder messages.",
    brief="Deactivates the bot"
)
async def off(ctx):
    usr, usr_id, usr_settings = _get_user_and_settings(ctx)
    is_active = usr_settings["is_active"]

    if is_active:
        remind_user.cancel()
        db.update({"is_active": False, "skip_first": True}, usr.id == usr_id)
        await ctx.send(Msg.Off.inactive)
    else:
        await ctx.send(Msg.Off.already_inactive)


@client.command(
    help="Sets a custom remind time. Provide the time for the desired remind interval in minutes after the command.",
    brief="Sets a custom remind time"
)
async def set_time(ctx, minutes):
    try:
        minutes = int(minutes)
        usr, usr_id, usr_settings = _get_user_and_settings(ctx)
        remind_user.change_interval(minutes=minutes)
        db.update({"reminder_minutes": minutes}, usr.id == usr_id)
        await ctx.send(Msg.SetTime().success(minutes))
    except ValueError:
        await ctx.send(Msg.SetTime.failure)


@client.command(
    help="This command will provide you further information about the bot, mainly what it is supposed to do.",
    brief="Provides further information about the bot"
)
async def info(ctx):
    await ctx.send(Msg.Information().message(NAME, REMINDER_MINUTES))


@tasks.loop(minutes=REMINDER_MINUTES)
async def remind_user(ctx):
    usr, usr_id, usr_settings = _get_user_and_settings(ctx)
    skip_first = usr_settings["skip_first"]
    reminder_toggle = usr_settings["reminder_toggle"]

    if skip_first:
        db.update({"skip_first": False}, usr.id == usr_id)
        return

    if reminder_toggle:
        await _send_hydrate_reminder(ctx)
    else:
        await _send_stretch_reminder(ctx)

    db.update({"reminder_toggle": not reminder_toggle}, usr.id == usr_id)


async def _send_hydrate_reminder(ctx):
    messages = [
        Msg.HydrationMessages.message01,
        Msg.HydrationMessages.message02,
        Msg.HydrationMessages.message03,
        Msg.HydrationMessages.message04,
        Msg.HydrationMessages.message05
    ]
    await ctx.send(random.choice(messages))


async def _send_stretch_reminder(ctx):
    messages = [
        Msg.StretchMessages.message01,
        Msg.StretchMessages.message02,
        Msg.StretchMessages.message03,
        Msg.StretchMessages.message04,
        Msg.StretchMessages.message05
    ]
    await ctx.send(random.choice(messages))


def _get_user_and_settings(ctx):
    usr = Query()
    usr_id = int(ctx.author.id)
    usr_settings = db.get(usr.id == usr_id)

    if not usr_settings:
        _create_new_user(usr_id)
        usr_settings = db.get(usr.id == usr_id)

    return usr, usr_id, usr_settings


def _create_new_user(usr_id):
    db.insert(
        {
            "id": usr_id,
            "is_active": False,
            "skip_first": True,
            "reminder_toggle": False,
            "reminder_minutes": REMINDER_MINUTES
        }
    )


client.run(TOKEN)
