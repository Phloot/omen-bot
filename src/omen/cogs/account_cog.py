# src/cogs/account_cog.py
import discord
import logging
from discord.utils import get
from discord.ext import commands, tasks
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
        self.account_updater.add_exception_type(discord.app_commands.errors.CommandInvokeError)
        self.account_updater.start()

    @app_commands.command(name="register", description="Register your GW2 API key")
    async def register_token(self, interaction: discord.Interaction, api_key: str):
        await interaction.response.defer()
        # Check with GW2 api to verify key
        api = await self.api_session(api_key)

        token_info = api.token_info()

        if token_info.get('text') == "Invalid access token":
            await interaction.followup.send("Unable to validate API key. API may be down, or your key is invalid. Try again in a few minutes.", ephemeral=True)
            return

        uid, name = await self.account_info(api) 

        register = self.db_service.insert_user(interaction.user.id, api_key, uid, name)
        await interaction.followup.send("API key registered", ephemeral=True)

    @app_commands.command(name="unregister", description="Delete your currently registered GW2 API key")
    async def delete_token(self, interaction: discord.Interaction = None, user_id: str = None):
        self.db_service.delete_user_api_key(interaction.user.id)
        await interaction.response.send_message("API key deleted", ephemeral=True)

    # Collect relevant account info
    async def account_info(self, user_session):
        # Lets collect account info
        try:
            user_info = user_session.account()
            return user_info['id'], user_info['name']
        except Exception:
            self.logger.exception("Could not fetch account info!")
            return None, None
        
    # Return a GW2Wrapper object for a users API key
    async def api_session(self, api_key: str):
        return GW2Wrapper(api_key)

    # Ensure that info is up to date - names can change
    @tasks.loop(minutes=720.0, reconnect = True)
    async def account_updater(self):
        try:
            # Retrieve all users from the database
            users = self.db_service.get_all_users()
            updated_users = []

            guild = self.omen_bot.get_guild(self.configs['discord_guild']['guild_id'])
            applicant_role = get(guild.roles, id=self.configs['discord_roles']['applicant'])
            # Loop through each user in the database
            for user in users:
                user_does_not_exist = False
                # Check if the user is in the specified guild and has required role or higher
                discord_user = guild.get_member(int(user.discord_id))
                if not discord_user:
                    self.logger.warning(f"User {discord_user} does not exist in the server!")
                    user_does_not_exist = True
                elif not discord_user.top_role >= applicant_role:
                    self.logger.warning(f"{discord_user} does not have a top role > {self.configs['discord_roles']['applicant']}")
                    user_does_not_exist = True

                # Clean up if user does not exist
                if user_does_not_exist:
                    self.db_service.delete_user_api_key(user.discord_id)
                    self.logger.warning(f"{user.gw2_account_name} (ID: {user.discord_id}) no longer exists, deleting ...")
                    continue
                       
                # Retrieve the user's account information from the API
                gw2_api = await self.api_session(user.api_key)
                new_gw2_account_id, new_gw2_account_name = await self.account_info(gw2_api)
                
                # Check if the user's account information has changed
                if new_gw2_account_id and new_gw2_account_name and (new_gw2_account_id != user.gw2_account_id or new_gw2_account_name != user.gw2_account_name):
                    # Update the user's information in the database
                    self.insert_user(user.discord_id, user.api_key, new_gw2_account_id, new_gw2_account_name)
                    updated_users.append(user)
            self.logger.info(f"Updated users in DB: {updated_users}")
        except Exception as e:
            self.logger.exception(f"Error in account_updater loop: {e}")

    @account_updater.before_loop
    async def before_account_updater(self):
        await self.omen_bot.wait_until_ready()

    async def cog_unload(self):
        self.account_updater.cancel()

async def setup(omen_bot):
    await omen_bot.add_cog(AccountCog(omen_bot))
