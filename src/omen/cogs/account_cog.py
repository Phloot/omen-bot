# src/cogs/account_cog.py
import discord
import logging
from discord.ext import commands
from functions import return_config, attach_image

from api.gw2_api import GW2Wrapper

"""
Cog: AccountCog
Description: Used to handle requests against GW2 accounts, starting with my own.
"""
class AccountCog(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")
        self.gw2_api = GW2Wrapper()

    # @commands.command()
    # async def account(self, ctx, member: discord.Member = None):
    #     self.logger.warning(f"{self.gw2_api.account()}")


async def setup(omen_bot):
    await omen_bot.add_cog(AccountCog(omen_bot))