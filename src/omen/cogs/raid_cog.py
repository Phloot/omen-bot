#https://jsoneditoronline.org/#left=url.https%3A%2F%2Fdps.report%2FgetJson%3Fpermalink%3DBQ3O-20230510-192157_wvw
# src/cogs/raid_cog.py
import discord
import logging
from discord.ext import commands
from discord import app_commands
from functions import return_config
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

    # Monitor #wvw-logs channel
    ## Parse stats
    ## Register them into a table - created based on raid UID 
    ### UID should be repeatable in the event of disconnect
    ### There should be an additional table that documents raids and whether theyre active or not
    #### Close out 'active' raids if their table hasn't had any new entries in ~30 minutes or when raid stop command is used
    ## Have stop/start command that commanders can use to initialize a raid
    ## Validate logs - ensure they're not old and haven't been registered yet
    ## Biggest Planker, Deadliest, Biggest Spikes, Cleanliest, Medic, Dodger, Magnet
    ## Give role to member for + awards
    