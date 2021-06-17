import discord
import json
import os
from discord.ext import commands
#from oasis_bot import OasisBot

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'configs/config.json')

    config_json_file = open(config_path,)
    config = json.load(config_json_file)
    config_json_file.close()

    #oasis_client = OasisBot()
    #oasis_client.run(config['authentication']['discord_token'])

    oasis_bot = commands.Bot(command_prefix='!')
    oasis_bot.load_extension("cogs.new_user_cog")
    oasis_bot.run(config['authentication']['discord_token'])