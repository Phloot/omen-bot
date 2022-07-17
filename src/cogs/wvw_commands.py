# src/cogs/wvw_commands.py
import os
import sys
import discord
import logging
from discord.ext import commands
from functions import to_lower

from api.gw2_api import GW2Wrapper

class WVWCommands(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.logger = logging.getLogger("omen_bot_logger")
        self.gw2_api = GW2Wrapper()
    
    @commands.command()
    async def worldpop(self, ctx, region: to_lower="na", member: discord.Member = None):
        world_list_all = self.gw2_api.worlds()

        if region == "na":
            flag_thumb = "https://i.imgur.com/vy8vgnr.png"
            bar_color = 0xff0000
            world_list_region = [world for world in world_list_all if world['id'] < 2000]
        elif region == "eu":
            flag_thumb = "https://imgur.com/Ajzamzu.png"
            bar_color = 0xffd700
            world_list_region = [world for world in world_list_all if world['id'] > 2000]
        
        embed=discord.Embed(title="{0} Server Populations".format(region.upper()), color=bar_color)
        embed.set_thumbnail(url=flag_thumb)
        embed.add_field(name=":red_circle: Full", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Full"]))
        embed.add_field(name=":orange_circle: Very High", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "VeryHigh"]))
        embed.add_field(name=":yellow_circle: High", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "High"]))
        embed.add_field(name=":green_circle: Medium", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Medium"]))
        #embed.add_field(name=":green_circle: Low", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Low"]))

        await ctx.channel.send(embed=embed)

def setup(omen_bot):
    omen_bot.add_cog(WVWCommands(omen_bot))