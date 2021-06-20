# src/cogs/wvw_commands.py
import os
import sys
import discord
import logging
from discord.ext import commands

from api.gw2_api import GW2Wrapper

class WVWCommands(commands.Cog):
    def __init__(self, oasis_bot):
        self.oasis_bot = oasis_bot
        self.logger = logging.getLogger("oasis_bot_logger")
        self.gw2_api = GW2Wrapper()
    
    @commands.command()
    async def worlds(self, ctx, *, member: discord.Member = None):
        self.logger.info(self.gw2_api.worlds())

def setup(oasis_bot):
    oasis_bot.add_cog(WVWCommands(oasis_bot))