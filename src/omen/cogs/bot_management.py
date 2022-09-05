# src/cogs/bot_management.py
import os
import sys
import discord
import logging
import socket
import platform
import datetime
from datetime import datetime, timedelta
from functions import convert_timedelta, return_config, attach_image
from discord.ext import commands

class BotManagement(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, member: discord.Member = None):
        cog_counter = 0
        base_dir = os.path.abspath(sys.path[0])
        cog_path = os.path.join(base_dir, 'cogs')

        for file in os.listdir(cog_path):
            if file.endswith('.py'):
                await self.omen_bot.reload_extension(f"cogs.{file.replace('.py', '')}")
                cog_counter+=1

        await ctx.channel.send(f"Reloaded {cog_counter} cog(s)")

    @commands.command()
    async def info(self, ctx, *, member: discord.Member = None):
        author_thumb = "bot_icon.png"

        try:
            info={}
            info['platform'] = platform.system() # Linux
            info['platform-release'] = platform.release() # Version
            info['architecture'] = platform.machine() # Architecture
            info['hostname'] = socket.gethostname() # Hostname
            info['processor'] = platform.processor() # Processor
        except Exception as sysinfo_ex:
            self.logger.warning(f"Error retrieving system info: {sysinfo_ex}")

        info['ping'] = f'{round(self.omen_bot.latency * 1000)}ms' # Ping

        # Generate uptime
        time_diff = datetime.now() - self.omen_bot.start_time
        hours, minutes, seconds = convert_timedelta(time_diff)
        info['uptime'] = f"{time_diff.days}d {int(hours) - (time_diff.days * 24)}h {int(minutes)}m"
        
        # Fetch version
        info['version'] = self.configs['internal']['version']

        # Fill in missing data
        for k, v in info.items():
            if v == "":
                info[k] = "Unknown"

        # Build and send embed
        author_img = attach_image(author_thumb)
        embed=discord.Embed(title="Bot Info", color=0xf0f0f0)
        embed.set_author(name=f"Omen Bot {info['version']}", url="https://github.com/Phloot/omen-bot", icon_url=f"attachment://{author_thumb}")
        embed.add_field(name="Uptime", value=f"{info['uptime']}")
        embed.add_field(name="Ping", value=f"{info['ping']}")
        embed.add_field(name="Hostname", value=f"{info['hostname']}")
        embed.add_field(name="Platform", value=f"{info['platform']} {info['platform-release']}")
        embed.add_field(name="Architecture", value=f"{info['architecture']}")
        embed.add_field(name="Processor", value=f"{info['processor']}")
        await ctx.channel.send(files=[author_img], embed=embed)

async def setup(omen_bot):
    await omen_bot.add_cog(BotManagement(omen_bot))