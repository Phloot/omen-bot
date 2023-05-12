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
Description: Used to handle requests against GW2 accounts, starting with DB implementation.
"""
class AccountCog(commands.GroupCog, name="account"):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")
        self.gw2_api = GW2Wrapper()
        self.db_service = DbService()

    @app_commands.command(name="register", description="Register your GW2 API key")
    async def register_token(self, interaction: discord.Interaction, api_key: str):
        # Check with GW2 api to verify key
        api = GW2Wrapper(api_key)

        token_info = api.token_info()

        if token_info.get('text') == "Invalid access token":
            await interaction.response.send_message("Unable to validate API key. API may be down, or your key is invalid. Try again in a few minutes.", ephemeral=True)
            return

        uid, name = await self.account_info(api) 

        register = self.db_service.insert_user(interaction.user.id, api_key)
        await interaction.response.send_message("API key registered", ephemeral=True)

    @app_commands.command(name="unregister", description="Delete your currently registered GW2 API key")
    async def delete_token(self, interaction: discord.Interaction):
        delete = self.db_service.delete_user_api_key(interaction.user.id)
        await interaction.response.send_message("API key deleted", ephemeral=True)

    # Collect relevant account info
    async def account_info(self, user_session: GW2Wrapper):
        # Lets collect account info
        try:
            user_info = user_session.account()
            return user_info['id'], user_info['name']
        except Exception:
            self.logger.exception("Could not fetch account info!")
            return None, None

    # Account wvwinfo

async def setup(omen_bot):
    await omen_bot.add_cog(AccountCog(omen_bot))
