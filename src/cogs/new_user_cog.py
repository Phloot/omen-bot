# src/cogs/new_user_cog.py
from discord.ext import commands

class NewUserCog:
    def __init__(self, oasis_bot):
        self.oasis_bot = oasis_bot

    async def on_message(self, message):
        print(message.content)

def setup(oasis_bot):
    oasis_bot.add_cog(NewUserCog(oasis_bot))