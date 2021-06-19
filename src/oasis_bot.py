import discord
import logging
import logging.config
import json
import sys
import os
from discord.ext import commands
from discord.ext.commands import NotOwner
from functions import return_config

if __name__ == "__main__":
    # General variables
    cog_counter = 0

    # Define logger
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Initialize bot and assign intents
    intents = discord.Intents.default()
    oasis_bot = commands.Bot(command_prefix='!', intents=intents)
    intents.members = True
    intents.presences = True

    # Load cogs
    base_dir = os.path.abspath(sys.path[0])
    cog_path = os.path.join(base_dir, 'cogs')

    for file in os.listdir(cog_path):
        if file.endswith('.py'):
            oasis_bot.load_extension("cogs.{0}".format(file.replace(".py", "")))
            cog_counter+=1

    # For exceptions caused through decorator perms, we need
    # to use a custom error handler as the library does not
    # provide a means to handling these errors
    @oasis_bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, NotOwner):
            print("User is not owner: {0}".format(str(error)))

    @oasis_bot.event
    async def on_ready():
        print("\nName: {0}\nID: {1}\nCog(s): {2}\nPing: {3}ms\n".format
        (
            oasis_bot.user.name,
            oasis_bot.user.id,
            cog_counter,
            round(oasis_bot.latency * 1000)
            )
        )  
        return

    # Run bot
    oasis_bot.run(return_config()['authentication']['discord_token'])