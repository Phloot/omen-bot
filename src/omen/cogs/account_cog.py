# src/cogs/account_cog.py
import discord
import logging
from discord.ext import commands
from discord import app_commands
from functions import return_config
from services.db_service import DbService

from api.gw2_api import GW2Wrapper

"""
Cog: AccountCog
Description: Used to handle requests against GW2 accounts, starting with my own.
"""
class AccountCog(commands.GroupCog, name="account"):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")
        self.gw2_api = GW2Wrapper()
        self.dbService = DbService()

    @app_commands.command(name="register_api_key", description="Register your GW2 API key")
    async def register_token(self, interaction: discord.Interaction, api_key: str):
        # Check with GW2 api to verify key
        api = GW2Wrapper(api_key)

        token_info = api.token_info()

        if token_info.get('text') == "Invalid access token":
            interaction.response.send_message("Invalid access token", ephemeral=True)

        self.dbService.insert_user(interaction.user.id, api_key)
        await interaction.response.send_message("API key registered", ephemeral=True)


    @app_commands.command(name="delete_api_key", description="Delete your currently registered GW2 API key")
    async def delete_token(self, interaction: discord.Interaction):
        self.dbService.delete_user_api_key(interaction.user.id)
        await interaction.response.send_message("API key deleted", ephemeral=True)

async def setup(omen_bot):
    await omen_bot.add_cog(AccountCog(omen_bot))