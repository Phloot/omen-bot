import discord
import json
import os
from discord.ext import commands

if __name__ == "__main__":
    # Pre bot launch configuration 
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'configs/config.json')

    config_json_file = open(config_path,)
    config = json.load(config_json_file)
    config_json_file.close()

    # Initialize bot and assign intents
    intents = discord.Intents.default()
    oasis_bot = commands.Bot(command_prefix='!', intents=intents)
    intents.members = True
    intents.presences = True
    
    @oasis_bot.event
    async def on_ready():
        print(f'\n\nName: {oasis_bot.user.name}\nID: {oasis_bot.user.id}\nStatus: Ready\n----------------------\n')  
        return

    # Load cogs
    oasis_bot.load_extension("cogs.new_user_cog")

    # Run bot
    oasis_bot.run(config['authentication']['discord_token'])