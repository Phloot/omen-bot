import discord
import json
import os
from discord.ext import commands
from functions import return_config

if __name__ == "__main__":
    # Initialize bot and assign intents
    intents = discord.Intents.default()
    omen_bot = commands.Bot(command_prefix='!', intents=intents)
    intents.members = True
    intents.presences = True
    
    @omen_bot.event
    async def on_ready():
        print(f'\n\nName: {omen_bot.user.name}\nID: {omen_bot.user.id}\nStatus: Ready\n----------------------\n')  
        return

    # Load cogs
    omen_bot.load_extension("cogs.new_user_cog")

    # Run bot
    omen_bot.run(return_config()['authentication']['discord_token'])