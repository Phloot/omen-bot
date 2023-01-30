import asyncio
import discord
import logging
import logging.config
import argparse
import datetime
import json
import sys
import os
from discord.ext import commands
from discord import app_commands
from functions import return_config
from services.db_service import DbService

if __name__ == "__main__":
    # Capture arguments
    parser = argparse.ArgumentParser(description='Capture script arguments.')
    parser.add_argument('--discord_token', type=str, nargs='?', const=None, default=None, help='Discord bot token') # will be accesible under args.discord_token
    args = parser.parse_args()

    # Define logger
    logger = logging.getLogger("omen_bot_logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)-3s] %(levelname)-3s %(module)s %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Initialize bot and assign intents
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True
    intents.message_content = True
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

    @omen_bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        await interaction.response.send_message(f"{interaction.user.name} failed to execute {interaction.command.name}! Reason: {error}")

    @omen_bot.event
    async def on_ready():
        omen_bot.start_time = datetime.datetime.now()
        await load_cogs()
        await omen_bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="over CO")
        )
        synced_commands = await omen_bot.tree.sync()
        logger.info(f"Slash commands synced: {len(synced_commands)}")
        logger.info(f"Name: {omen_bot.user.name}")
        logger.info(f"ID: {omen_bot.user.id}")
        logger.info(f"Ping: {round(omen_bot.latency * 1000)}ms")
        logger.info("Bot is ready!")
        return

    # Run bot
    omen_bot.run(token=os.environ['DISCORD_TOKEN'] if not None else args.discord_token)