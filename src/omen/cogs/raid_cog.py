#https://jsoneditoronline.org/#left=url.https%3A%2F%2Fdps.report%2FgetJson%3Fpermalink%3DBQ3O-20230510-192157_wvw
#https://dps.report/getJson?permalink=niAH-20220816-203824_void
# src/cogs/raid_cog.py
import re
import discord
import logging
import requests
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from functions import return_config, attach_image
from services.db_service import DbService

from api.gw2_api import GW2Wrapper

"""
Cog: RaidCog
Description: Used to process raid logs and provide WvW raid specific data
"""
class RaidCog(commands.GroupCog, name="raid"):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")

    async def analyze_links(self, message):
        pattern = re.compile(r"(?:https?:\/\/)?(?:wvw|dps)\.report\/(?:w\.report\/)?([A-Za-z0-9_-]+)")
        # Find all links in the message content using the pattern
        links = re.findall(pattern, message.content)
        if links:
            # If links were found, analyze them here
            for link in links:
                report_id = link.split('/')[-1]
                self.logger.info(f'Found Report ID: {report_id}')

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message was sent in the specific channel you want to monitor
        if message.channel.id == self.configs['discord_channels']['wvw_logs']:
            # Compile regular expression pattern to match links
            await self.analyze_links(message)
    
    # Simple function to return easily readable fight report in json format
    async def json_report_url(self, report_id):
        return f"https://dps.report/getJson?permalink={report_id}"
    
    # Collect WvW report json 
    async def collect_json_report(self, json_url):
        response = requests.get(json_url)
        return response.json() 
            
    # Check to use in raid stop/start decorators
    @staticmethod
    async def can_command(interaction: discord.Interaction):
        commander_role = get(interaction.guild.roles, name="Commander")
        return interaction.user.top_role >= commander_role
    
    @app_commands.command(name="start", description="Start a raid")
    @app_commands.check(can_command)
    @app_commands.describe(map="Select a map")
    @app_commands.choices(map=[
        app_commands.Choice(name="Eternal Battlegrounds", value="ebg"),
        app_commands.Choice(name="Green Borderland", value="gbl"),
        app_commands.Choice(name="Red Borderland", value="rbl"),
        app_commands.Choice(name="Blue Borderland", value="bbl")
    ])
    @app_commands.describe(timezone="Select a timezone to highlight")
    @app_commands.choices(timezone=[
        app_commands.Choice(name="North America", value="na"),
        app_commands.Choice(name="Europe", value="eu"),
        app_commands.Choice(name="Oceanic", value="ocx"),
        app_commands.Choice(name="Southeast Asia", value="sea")
    ])
    async def start_raid(self, interaction: discord.Interaction, map: app_commands.Choice[str], timezone: app_commands.Choice[str]):
        maps = {
            "ebg": {"sidebar_hex": 0xfdfefe},
            "gbl": {"sidebar_hex": 0x2ecc71},
            "rbl": {"sidebar_hex": 0xe74c3c},
            "bbl": {"sidebar_hex": 0x3498db}
        }
        commander_emoji = "<:commander:989618091317137429>"
        map_img = f"{map.value}_map.png"
        map_img_attached = attach_image(map_img)
        self.logger.info(f"Will begin a(n) {timezone} raid on {map}, lead by commander {interaction.user}")

        tz_role = interaction.guild.get_role(int(self.configs['discord_roles'][timezone.value]))

        embed=discord.Embed(title=f"A WvW raid is beginning!", color=maps[map.value]["sidebar_hex"])
        embed.set_author(name=interaction.user.display_name, url="https://wvwstats.com/na", icon_url=interaction.user.display_avatar)
        embed.set_thumbnail(url=f"attachment://{map_img}")
        embed.add_field(name="Commander", value=f"{commander_emoji} {interaction.user.display_name}")
        embed.add_field(name="Map", value=map.name)
        embed.add_field(name="Timezone", value=timezone.name)
        await interaction.response.send_message(
            files=[map_img_attached], 
            embed=embed, 
            content=tz_role.mention,
            allowed_mentions=discord.AllowedMentions(everyone=True, roles=True)
            )
        

    @app_commands.command(name="stop", description="Stop a raid")
    async def end_raid(self, raid_to_stop):
        pass


    ## Parse stats
    ## Register them into a table - created based on raid UID 
    ### UID should be repeatable in the event of disconnect
    ### There should be an additional table that documents raids and whether theyre active or not
    #### Close out 'active' raids if their table hasn't had any new entries in ~30 minutes or when raid stop command is used
    ## Have stop/start command that commanders can use to initialize a raid
    ## Validate logs - ensure they're not old and haven't been registered yet
    ## Biggest Planker, Deadliest, Biggest Spikes, Cleanliest, Medic, Dodger, Magnet
    ## Give role to member for + awards
    
async def setup(omen_bot):
    await omen_bot.add_cog(RaidCog(omen_bot))
