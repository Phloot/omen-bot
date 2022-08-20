import asyncio
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
    parser.add_argument('--discord_token', type=str, help='Discord bot token') # will be accesible under args.discord_token
    args = parser.parse_args()

    # Define logger
    logger = logging.getLogger("omen_bot_logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)-3s] %(levelname)-3s %(module)s %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Initialize bot and assign intents
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    omen_bot = commands.Bot(command_prefix='!', intents=intents)

    # Load cogs
    async def load_cogs():
        cog_counter = 0

        # OS agnostic pathing
        base_dir = os.path.abspath(sys.path[0])
        cog_path = os.path.join(base_dir, 'cogs')

        # Load cogs
        for file in os.listdir(cog_path):
            if file.endswith('.py'):
                await omen_bot.load_extension(f"cogs.{file.replace('.py', '')}")
                cog_counter+=1

        logger.info(f"Cog(s): {cog_counter}")

    # For exceptions caused through decorator perms, we need
    # to use a custom error handler as the library does not
    # provide a means to handling these errors
    @omen_bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, NotOwner):
            logger.warning(f"{ctx.author.name} attempted to execute command restricted to bot owner")

    @omen_bot.event
    async def on_ready():
        await omen_bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="over CO")
        )
        await load_cogs()
        logger.info(f"Name: {omen_bot.user.name}")
        logger.info(f"ID: {omen_bot.user.id}")
        logger.info(f"Ping: {round(omen_bot.latency * 1000)}ms")
        logger.info("Bot is ready!")
        return

    # Run bot
    omen_bot.run(token=args.discord_token)