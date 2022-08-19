import discord
import logging
import logging.config
import argparse
import json
import sys
import os
from discord.ext import commands
from discord.ext.commands import NotOwner
from functions import return_config

if __name__ == "__main__":
    # Capture arguments
    parser = argparse.ArgumentParser(description='Capture script arguments.')
    parser.add_argument('--discord_token', type=str, help='Discord not token') # will be accesible under args.discord_token
    args = parser.parse_args()

    # General variables
    cog_counter = 0

    # Define logger
    logger = logging.getLogger("omen_bot_logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)-3s] %(levelname)-3s %(module)s %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Initialize bot and assign intents
    intents = discord.Intents.default()
    omen_bot = commands.Bot(command_prefix='!', intents=intents)
    intents.members = True
    intents.presences = True

    # Load cogs
    base_dir = os.path.abspath(sys.path[0])
    cog_path = os.path.join(base_dir, 'cogs')

    for file in os.listdir(cog_path):
        if file.endswith('.py'):
            omen_bot.load_extension("cogs.{0}".format(file.replace(".py", "")))
            cog_counter+=1

    # For exceptions caused through decorator perms, we need
    # to use a custom error handler as the library does not
    # provide a means to handling these errors
    @omen_bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, NotOwner):
            logger.warning("{0} attempted to execute command restricted to bot owner".format(ctx.author.name))

    @omen_bot.event
    async def on_ready():
        logger.info("Name: {0}".format(omen_bot.user.name))
        logger.info("ID: {0}".format(omen_bot.user.id))
        logger.info("Cog(s): {0}".format(cog_counter))
        logger.info("Ping: {0}ms".format(round(omen_bot.latency * 1000)))
        logger.info("Bot is ready!")
        return

    # Run bot
    omen_bot.run(args.discord_token)