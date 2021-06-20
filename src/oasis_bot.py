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
    logger = logging.getLogger("oasis_bot_logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)-3s] %(levelname)-3s %(module)s %(message)s', "%Y-%m-%d %H:%M:%S")
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
            logger.warning("{0} attempted to execute command restricted to bot owner".format(ctx.author.name))

    @oasis_bot.event
    async def on_ready():
        logger.info("Bot is ready")
        logger.info("Name: {0}".format(oasis_bot.user.name))
        logger.info("ID: {0}".format(oasis_bot.user.id))
        logger.info("Cog(s): {0}".format(cog_counter))
        logger.info("Ping: {0}ms".format(round(oasis_bot.latency * 1000)))
        return

    # Run bot
    oasis_bot.run(return_config()['authentication']['discord_token'])