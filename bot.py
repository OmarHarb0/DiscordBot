import discord
from discord.ext import commands
import os
from Classes import database
import asyncpg
import passwords

TOKEN = os.environ['DC_BOT_TOKEN']


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ["!"]

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = [
    'cogs.spam', 'cogs.owner', 'cogs.voice_commands', 'cogs.steamdata', 'cogs.dotastats'
]


bot = commands.Bot(command_prefix=get_prefix, description='Asd')
db = 'dotaheroes'
db_user = 'postgres'
db_host = 'localhost'
db_password = passwords.sqlpass

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    bot.pool = await asyncpg.create_pool(database=db,
                                           user=db_user,
                                           host=db_host,
                                           loop=bot.loop,
                                           password=db_password,
                                           max_inactive_connection_lifetime=600,
                                           min_size=10,
                                           max_size=20)
    bot.db = database.DatabaseUtils(bot)

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Quran"))
    print(f'Successfully logged in and booted...!')


@bot.event
async def on_disconnect():
    print("DISCONNECTED")


bot.run(TOKEN, bot=True, reconnect=True)

