# src/cogs/bot_management.py
import os
import sys
import discord
import logging
from discord.ext import commands

class BotManagement(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.logger = logging.getLogger("omen_bot_logger")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, member: discord.Member = None):
        cog_counter = 0
        base_dir = os.path.abspath(sys.path[0])
        cog_path = os.path.join(base_dir, 'cogs')

        for file in os.listdir(cog_path):
            if file.endswith('.py'):
                await self.omen_bot.reload_extension("cogs.{0}".format(file.replace(".py", "")))
                cog_counter+=1

        await ctx.channel.send("Reloaded {0} cog(s)".format(cog_counter))

async def setup(omen_bot):
    await omen_bot.add_cog(BotManagement(omen_bot))