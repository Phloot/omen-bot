# src/cogs/guild_organization.py
import discord
import logging
from discord.ext import commands
from functions import return_config, attach_image

"""
Cog: GuildOrganizationCog
Description: Used to provide organization value to the server such as 
raid scheduling and other helpful functions.
"""
class GuildOrganizationCog(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")

async def setup(omen_bot):
    await omen_bot.add_cog(GuildOrganizationCog(omen_bot))