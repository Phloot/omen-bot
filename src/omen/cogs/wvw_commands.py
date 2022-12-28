# src/cogs/wvw_commands.py
import os
import sys
import discord
import logging
import json
from discord.ext import commands
from functions import to_lower, attach_image

from api.gw2_api import GW2Wrapper

class WVWCommands(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.logger = logging.getLogger("omen_bot_logger")
        self.gw2_api = GW2Wrapper()
        self.img_world_population = "world_population.png"

    async def get_current_victory_points(self):
        return

    async def get_current_kdr(self):
        return

    async def get_current_match_servers(self):
        return

    async def get_current_match_data(self):
        return self.gw2_api.wvw_matches(await self.get_current_world())

    async def get_current_world(self):
        return self.gw2_api.account()['world']

    @commands.command()
    async def matchup(self, ctx, member: discord.Member = None):
        # Current victory points for each server

        # Current k/d for each server

        # Current objectives for each server
        await self.build_objectives_dictionary()
        return
    
    @commands.command()
    async def worldpop(self, ctx, region: to_lower="na", member: discord.Member = None):
        img_flag = f"flag_{region}.png"
        world_list_all = self.gw2_api.worlds()

        if region == "na":
            bar_color = 0x0c09ec
            world_list_region = [world for world in world_list_all if world['id'] < 2000]
        elif region == "eu":
            bar_color = 0xffd700
            world_list_region = [world for world in world_list_all if world['id'] > 2000]
        
        # Attach images to display
        author_img = attach_image(img_flag)
        thumbnail_img = attach_image(self.img_world_population)

        # Initialize the embed
        embed=discord.Embed(title=f"Worlds", color=bar_color)
        embed.set_author(name=f"Current {region.upper()} World Populations", icon_url=f"attachment://{img_flag}")
        embed.set_thumbnail(url=f"attachment://{self.img_world_population}")
        embed.add_field(name=":red_circle: Full", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Full"]))
        embed.add_field(name=":orange_circle: Very High", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "VeryHigh"]))
        embed.add_field(name=":yellow_circle: High", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "High"]))
        embed.add_field(name=":green_circle: Medium", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Medium"]))
        #embed.add_field(name=":green_circle: Low", value='\n'.join([world['name'] for world in world_list_region if world['population'] == "Low"]))

        await ctx.channel.send(files=[author_img, thumbnail_img], embed=embed)

async def setup(omen_bot):
    await omen_bot.add_cog(WVWCommands(omen_bot))