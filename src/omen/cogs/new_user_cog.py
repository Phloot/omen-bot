# src/cogs/new_user_cog.py
import discord
import logging
from discord.ext import commands
from functions import return_config

"""
Cog: NewUserCog
Description: Used to handle member join events, by welcoming them in the system
channel and sending them a direct message with more information.
"""
class NewUserCog(commands.Cog):
    def __init__(self, omen_bot):
        self.omen_bot = omen_bot
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        # Send a welcome message to the system channel
        if channel is not None:
            await channel.send(f"Welcome to [CO], {member.mention}! Please check out {self.omen_bot.get_channel(self.configs['discord_channels']['role_selection']).mention} \
            to choose roles and {self.omen_bot.get_channel(self.configs['discord_channels']['meta_builds']).mention} if you're looking for squad builds.")
        
        # Send a direct message to the user
        embed=discord.Embed(title="Celestial Omen", description="A Crystal Desert community guild for pugs and pugmanders", color=0x2974ff)
        embed.set_author(name="Omen", icon_url="https://i.imgur.com/mJHFxWq.png")
        embed.set_thumbnail(url="https://i.imgur.com/xR7N7aQ.gif")
        embed.add_field(name="Overview", value="Welcome to the Celestial Omen Discord! We're a guild focused on off-hours raiding\
            and content. We aim to bring together pugs and pugmanders from all sorts of timezones and guilds so as to build\
            a formidable force outside of the standard NA timezone raids.", inline=False)
        embed.add_field(name="Join the Community", value=f"We're always open to welcome in new members, and with our minimal\
            requirements, you may find that [CO] is the perfect complement to your primary NA timezone guild. Interested\
            in joining the squad? Check out {self.omen_bot.get_channel(self.configs['discord_channels']['join_channel']).mention} for details.", inline=False
            )
        embed.add_field(name="Additional Info", value=f"If you have any questions about your class, or would like to have 1 on 1\
            discussions about the classes that you play, we'd love to help. Feel free to reach out to any **__Organizer__** or \
            **__Advisor__** for info, and check out {self.omen_bot.get_channel(self.configs['discord_channels']['meta_builds']).mention} for helpful builds."
            )
        embed.set_footer(text="Thanks, [CO] leadership team")

        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            self.logger.warning(f"{member} is not accepting direct messages at this time")
        except discord.DiscordException as gen_ex:
            self.logger.warning(f"Failed to direct message new user ({str(gen_ex)})")


async def setup(omen_bot):
    await omen_bot.add_cog(NewUserCog(omen_bot))
