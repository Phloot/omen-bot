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
        self.server_colors = [ 'green', 'blue', 'red' ]

        # Internal dictionary to house match data - not required, but helpful to visualize
        self.match_data_dict = {
            'tier': '',
            'blue': {
                'worlds': {
                    'host': '',
                    'link': ''
                },
                'victory_points': 0,
                'kd': {
                    'kills': 0,
                    'deaths': 0,
                    'kdr': 0
                },
                'objectives': {
                    'camp': 0,
                    'tower': 0,
                    'keep': 0,
                    'castle': 0
                }
            },
            'green': {
                'worlds': {
                    'host': '',
                    'link': ''
                },
                'victory_points': 0,
                'kd': {
                    'kills': 0,
                    'deaths': 0,
                    'kdr': 0
                },
                'objectives': {
                    'camp': 0,
                    'tower': 0,
                    'keep': 0,
                    'castle': 0
                }
            },
            'red': {
                'worlds': {
                    'host': '',
                    'link': ''
                },
                'victory_points': 0,
                'kd': {
                    'kills': 0,
                    'deaths': 0,
                    'kdr': 0
                },
                'objectives': {
                    'camp': 0,
                    'tower': 0,
                    'keep': 0,
                    'castle': 0
                },
            }
        }

    # Populate class dictionary with VP data
    async def get_current_victory_points(self, match_data):
        for server, points in match_data['victory_points'].items():
            try:
                self.match_data_dict[server]['victory_points'] = points
            except Exception as e:
                self.match_data_dict[server]['victory_points'] = self.match_data_dict[server]['victory_points']

    # Populate class dictionary with K/D data
    async def get_current_kdr(self, match_data):
        # Collect kills
        for server, k_or_d in match_data['kills'].items():
            self.match_data_dict[server]['kd']['kills'] = k_or_d

        # Collect deaths
        for server, k_or_d in match_data['deaths'].items():
            self.match_data_dict[server]['kd']['deaths'] = k_or_d

        # Calc and store KDR
        for server, data in self.match_data_dict.items():
            try:
                if server in [ 'blue', 'green', 'red' ]:
                    self.match_data_dict[server]['kd']['kdr'] = round(data['kd']['kills'] / data['kd']['deaths'], 2) 
            except Exception as e:
                self.match_data_dict[server]['kd']['kdr'] = self.match_data_dict[server]['kd']['kdr']
                self.logger.error(f"Unable to calculate KDR in get_current_kdr: {e}")

    # Populate class dictionary with server data
    async def get_current_match_servers(self, match_data):
        for server, ids in match_data['all_worlds'].items():
            try:
                self.match_data_dict[server]['worlds']['host'] = self.gw2_api.worlds([ids[1]])[0]['name']
                self.match_data_dict[server]['worlds']['link'] = self.gw2_api.worlds([ids[0]])[0]['name']
            except Exception as e:
                self.logger.error(f"Problem in get_current_match_servers: {e}")

    # Populate class dictionary with owned objectives data
    async def get_owned_objectives(self, match_data):
        # We need to reset values in the self dict before proceeding since we are counting
        for s in self.server_colors:
            self.match_data_dict[s]['objectives'] = self.match_data_dict[s]['objectives'].fromkeys(self.match_data_dict[s]['objectives'], 0)

        objectives_to_count = [ 'camp', 'tower', 'keep', 'castle' ]
        map_count = len(match_data['maps'])
        map_iter = 0

        while map_iter < map_count:
            obj_count = len(match_data['maps'][map_iter]['objectives'])
            obj_iter = 0

            while obj_iter < obj_count:
                obj_owner = match_data['maps'][map_iter]['objectives'][obj_iter]['owner'].lower()
                obj_type = match_data['maps'][map_iter]['objectives'][obj_iter]['type'].lower()

                try:
                    if obj_type in objectives_to_count: self.match_data_dict[obj_owner]['objectives'][obj_type] += 1
                except Exception as e:
                    print(e)
                obj_iter += 1
            map_iter += 1

    # Return tier for current matchup
    async def get_current_tier(self, match_data):
        self.match_data_dict['tier'] = match_data['id'].split('-')[1]

    # Generic function to get full WvW data for current match
    async def get_current_match_data(self):
        try:
            return self.gw2_api.wvw_matches(await self.get_current_world())
        except Exception as e:
            self.logger.error(f"Unable to retrieve data in get_current_match_data: {e}")
            return None

    # Return current world for Rall
    async def get_current_world(self):
        try:
            return self.gw2_api.account()['world']
        except Exception as e:
            self.logger.error(f"Unable to retrieve data in get_current_world: {e}")
            return '1014'

    @commands.command()
    async def matchup(self, ctx, member: discord.Member = None):
        # General variables
        camp_emoji = "<:wvw_camp:1058165536334303272>"
        tower_emoji = "<:wvw_tower:1058167072762384414>"
        keep_emoji = "<:wvw_keep:1058165533532500108>"
        castle_emoji = "<:wvw_castle:1058165532366487572>"
        icon_image = "icon_author_co.jpg" 
        thumb_image = "wvw_thumbnail.png" 
        embed_obj_value_string = ""
        
        author_img_attached = attach_image("icon_author_co.jpg")
        thumb_img_attached = attach_image("wvw_thumbnail.png")

        # Retrieve match data and set initial data in dict
        match_data = await self.get_current_match_data()

        if match_data:
            await self.get_current_match_servers(match_data)
            await self.get_current_tier(match_data)
                    
            # Current victory points for each server
            await self.get_current_victory_points(match_data)

            # Current k/d for each server
            await self.get_current_kdr(match_data)

            # Current objectives for each server
            await self.get_owned_objectives(match_data)
        else:
            self.logger.error(f"Match data currently unavailable. API may be down!")
        
        embed=discord.Embed(title="Current Matchup", url="https://wvwintel.com/#1014", description=f"Tier {self.match_data_dict['tier']}", color=0xa8009a)
        embed.set_author(name="Omen", url="https://github.com/Phloot/omen-bot/", icon_url=f"attachment://{icon_image}")
        embed.set_thumbnail(url=f"attachment://{thumb_image}")
        for server in self.server_colors:
            embed.add_field(
                name=f":{server}_circle: {server.title()}", 
                value=f"{self.match_data_dict[server]['worlds']['host']}\n{self.match_data_dict[server]['worlds']['link']}\n\n"
                f"**Victory Points**: {self.match_data_dict[server]['victory_points']}\n**K/D**: {self.match_data_dict[server]['kd']['kdr']}", 
                inline=True
            )
            embed_obj_value_string += f":{server}_circle: {camp_emoji}x{self.match_data_dict[server]['objectives']['camp']:=2} {tower_emoji}x{self.match_data_dict[server]['objectives']['tower']:=2} {keep_emoji}x{self.match_data_dict[server]['objectives']['keep']:=2} {castle_emoji}x{self.match_data_dict[server]['objectives']['castle']:=2}\n"
        embed.add_field(name="Current Skirmish", value="blah blah", inline=False)
        embed.add_field(name="Objectives", value=embed_obj_value_string, inline=False)
        embed.set_footer(text="Data as of TBD")
        await ctx.channel.send(files=[author_img_attached, thumb_img_attached], embed=embed)
    
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