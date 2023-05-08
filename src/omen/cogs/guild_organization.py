# src/cogs/guild_organization.py
import discord
import logging
import math
import time
from discord.ext import commands
from discord import app_commands
import datetime
from functions import (
    return_config, 
    attach_image, 
    convert_timedelta,
    merge_dicts 
)

"""
Cog: GuildOrganizationCog
Description: Used to provide organization value to the server such as 
raid scheduling and other helpful functions.
"""
class GuildOrganization(commands.GroupCog, name="guild"):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")
        self.icon_image = "icon_author_co.jpg" 
        self.combined_schedules = {
            0: { "hour": 18, "minute": 30, "commander": "Thorton" }, # Monday
            1: { "hour": 18, "minute": 30, "commander": "Hells" },   # Tuesday
            2: { "hour": 18, "minute": 30, "commander": "Rall" },    # Wednesday
            4: { "hour": 20, "minute": 00, "commander": "Rall" },    # Friday
            5: { "hour": 12, "minute": 0,  "commander": "Rall" },    # Saturday
            6: { "hour": 18, "minute": 30, "commander": "Rall" }     # Sunday 
        }
        self.commander_emoji = "<:commander:989618091317137429>"

    # Given a list of days, find the nearest (future) day of week
    async def _nearest_date(self, items: list, pivot):
        return min(items, key=lambda x: abs(x - pivot))

    async def _get_timestamps_list(self):
        epoch_dict = {}
        next_raid_timedelta, next_raid_commander = await self._next_raid()
        upcoming_raid, commander = await self._next_raid(next_raid_timedelta + datetime.timedelta(days=1))

        x = 0
        while x < 3:
            raid_after_next_timedelta, raid_after_next_commander = await self._next_raid(upcoming_raid)
            epoch_dict.update({math.trunc(raid_after_next_timedelta.timestamp()): raid_after_next_commander})
            upcoming_raid, commander = await self._next_raid(upcoming_raid + datetime.timedelta(days=1))
            x += 1
        return "\n".join(f"<t:{r_time}:F> {self.commander_emoji}{r_cmd}" for r_time, r_cmd in epoch_dict.items())

    async def _next_raid(self, day_override = None):
        today = day_override.date() if day_override else datetime.date.today()
        day_list = []

        for day in self.combined_schedules.keys():
            days = (day - today.weekday() + 7) % 7
            day_list.append(today + datetime.timedelta(days=days))

        next = await self._nearest_date(day_list, today) 
        return datetime.datetime.fromordinal(next.toordinal()).replace(hour=self.combined_schedules[next.weekday()]["hour"], minute=self.combined_schedules[next.weekday()]["minute"]), f"{self.combined_schedules[next.weekday()]['commander']}"

    @app_commands.command(name="schedule", description="Display the guilds WvW schedule")
    async def schedule(self, interaction: discord.Interaction):
        next_raid, commander = await self._next_raid()
        next_raid_datetime = next_raid.replace(hour=self.combined_schedules[next_raid.weekday()]["hour"], minute=self.combined_schedules[next_raid.weekday()]["minute"])
        hours, minutes, seconds = convert_timedelta(next_raid - datetime.datetime.now())

        if -2 <= hours < 0:
            raid_status = "Raid is active!"
        elif -23 <= hours <= -3:
            raid_status = "Raid completed"
        else:
            raid_status = f"{math.floor(hours/24)}d {hours - (math.floor(hours/24)*24)}h {minutes}m"

        author_img_attached = attach_image(self.icon_image)
        thumbnail_img_attached = attach_image("calendar.png")

        embed=discord.Embed(title=f"[CO] Schedule", color=0xd122c4)
        embed.set_author(name="Omen", url="https://github.com/Phloot/omen-bot/", icon_url=f"attachment://{self.icon_image}")
        embed.set_thumbnail(url=f"attachment://calendar.png")
        embed.add_field(name="Next Raid", value=f"<t:{math.trunc(next_raid_datetime.timestamp())}:F> {self.commander_emoji}{commander}")
        embed.add_field(name="Time Until", value=f"{raid_status}")
        embed.add_field(name="Future Raids", value=f"{await self._get_timestamps_list()}", inline=False)
        embed.set_footer(text="Times are dynamic and are generated off of your personal timezone")
        await interaction.response.send_message(files=[author_img_attached, thumbnail_img_attached], embed=embed)

async def setup(omen_bot):
    await omen_bot.add_cog(GuildOrganization(omen_bot))