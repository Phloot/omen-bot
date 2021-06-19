import discord
import json
import sys
import os
from discord.ext import commands
from functions import return_config

if __name__ == "__main__":
    # General variables
    cog_counter = 0

    # Initialize bot and assign intents
    intents = discord.Intents.default()
    oasis_bot = commands.Bot(command_prefix='!', intents=intents)
    intents.members = True
    intents.presences = True
    
    @oasis_bot.event
    async def on_ready():
        print("\nName: {0}\nID: {1}\nCog(s): {2}\nPing: {3}ms\n".format
        (
            oasis_bot.user.name,
            oasis_bot.user.id,
            cog_counter,
            round(oasis_bot.latency * 1000)
            )
        )  
        return

    # Load cogs
    #oasis_bot.load_extension("cogs.new_user_cog")
    base_dir = os.path.abspath(sys.path[0])
    cog_path = os.path.join(base_dir, 'cogs')

    for file in os.listdir(cog_path):
        if file.endswith('.py'):
            oasis_bot.load_extension("cogs.{0}".format(file.replace(".py", "")))
            cog_counter+=1

    # Run bot
    oasis_bot.run(return_config()['authentication']['discord_token'])