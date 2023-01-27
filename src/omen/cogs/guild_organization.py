# src/cogs/guild_organization.py
import discord
import logging
import math
import time
from discord.ext import commands
from discord import app_commands
import datetime
from functions import return_config, attach_image, convert_timedelta

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
        self.rall_schedule = {
            0: { "hour": 18, "minute": 30 }, # Monday
            3: { "hour": 18, "minute": 30 }, # Thursday
            5: { "hour": 12, "minute": 0 },  # Saturday
            6: { "hour": 12, "minute": 0 }   # Sunday
        }

    async def _nearest_date(self, items, pivot):
        return min(items, key=lambda x: abs(x - pivot))

    async def _get_timestamps_list(self):
        epoch_list = []
        upcoming_raid = await self._next_raid(await self._next_raid() + datetime.timedelta(days=1))

        x = 0
        while x < 3:
            epoch_list.append(math.trunc((await self._next_raid(upcoming_raid)).timestamp()))
            upcoming_raid = await self._next_raid(upcoming_raid + datetime.timedelta(days=1))
            x += 1
        return "\n".join(f"<t:{item}:F>" for item in epoch_list)

    async def _next_raid(self, day_override = None):
        today = day_override.date() if day_override else datetime.date.today()
        day_list = []

        for day in self.rall_schedule.keys():
            days = (day - today.weekday() + 7) % 7
            day_list.append(today + datetime.timedelta(days=days))

        next = await self._nearest_date(day_list, today) 
        return datetime.datetime.fromordinal(next.toordinal()).replace(hour=self.rall_schedule[next.weekday()]["hour"], minute=self.rall_schedule[next.weekday()]["minute"])

    @app_commands.command(name="schedule", description="Diasplay the guilds WvW schedule")
    async def schedule(self, interaction: discord.Interaction):
        next_raid = await self._next_raid()
        hours, minutes, seconds = convert_timedelta(next_raid - datetime.datetime.now())
        print(f"hours {hours} minutes {minutes} seconds {seconds}")

        if -2 <= hours <= 0:
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
        embed.add_field(name="Next Raid", value=f"<t:{math.trunc(next_raid.timestamp())}:F>")
        embed.add_field(name="Time Until", value=f"{raid_status}")
        embed.add_field(name="Future Raids", value=f"{await self._get_timestamps_list()}", inline=False)
        embed.set_footer(text="Times are dynamic and are generated off of your personal timezone")
        await interaction.response.send_message(files=[author_img_attached, thumbnail_img_attached], embed=embed)

async def setup(omen_bot):
    await omen_bot.add_cog(GuildOrganization(omen_bot))