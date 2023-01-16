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
from discord import app_commands

class BotManagement(commands.GroupCog, name="manage"):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="reload", description="Reloads cogs to pull changes in")
    async def reload(self, interaction: discord.Interaction):
        cog_counter = 0
        base_dir = os.path.abspath(sys.path[0])
        cog_path = os.path.join(base_dir, 'cogs')

        for file in os.listdir(cog_path):
            if file.endswith('.py'):
                await self.omen_bot.reload_extension(f"cogs.{file.replace('.py', '')}")
                cog_counter+=1
        await interaction.response.send_message(f"Reloaded {cog_counter} cog(s)")

    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="info", description="Provides general bot info")
    async def info(self, interaction: discord.Interaction):
        icon_image = "icon_author_co.jpg" 

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
        author_img_attached = attach_image("icon_author_co.jpg")
        embed=discord.Embed(title="Bot Info", color=0xf0f0f0)
        embed.set_author(name="Omen", url="https://github.com/Phloot/omen-bot/", icon_url=f"attachment://{icon_image}")
        embed.add_field(name="Uptime", value=f"{info['uptime']}")
        embed.add_field(name="Ping", value=f"{info['ping']}")
        embed.add_field(name="Hostname", value=f"{info['hostname']}")
        embed.add_field(name="Platform", value=f"{info['platform']} {info['platform-release']}")
        embed.add_field(name="Architecture", value=f"{info['architecture']}")
        embed.add_field(name="Processor", value=f"{info['processor']}")
        await interaction.response.send_message(files=[author_img_attached], embed=embed)

async def setup(omen_bot):
    await omen_bot.add_cog(BotManagement(omen_bot))