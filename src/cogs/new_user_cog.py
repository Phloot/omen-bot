# src/cogs/new_user_cog.py
import discord
from discord.ext import commands
from functions import return_config

class NewUserCog(commands.Cog):
    def __init__(self, oasis_bot):
        self.oasis_bot = oasis_bot
        self.configs = return_config()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        # Send a welcome message to the system channel
        if channel is not None:
            await channel.send('Welcome to [CO], {0.mention}! Please check out {1.mention} and {2.mention} when you have time.'.format
            (
                member,
                self.oasis_bot.get_channel(self.configs['discord_channels']['role_selection']),
                self.oasis_bot.get_channel(self.configs['discord_channels']['community_info']),
                )
            )
        
        # Send a direct message to the user
        embed=discord.Embed(title="Crystal Oasis", description="A Crystal Desert community guild for pugs and pugmanders", color=0x2974ff)
        embed.set_author(name="Overseer of the Oasis", icon_url="https://i.imgur.com/mJHFxWq.png")
        embed.set_thumbnail(url="https://i.imgur.com/3nHcRTV.png")
        embed.add_field(name="Overview", value="Welcome to the Crystal Oasis Discord! We're a guild focused on off-hours raiding\
            and content. We aim to bring together pugs and pugmanders from all sorts of timezones and guilds so as to build\
            a formidable force outside of the standard NA timezone raids.", inline=False)
        embed.add_field(name="Join the Community", value="We're always open to welcome in new members, and with our minimal\
            requirements, you may find that [CO] is the perfect complement to your primary NA timezone guild. Interested\
            in joining the squad? Check out {0.mention} for details.".format
            (
                self.oasis_bot.get_channel(self.configs['discord_channels']['join_channel'])
                ), inline=False
            )
        embed.set_footer(text="- [CO] leadership team")
        await member.send(embed=embed)

def setup(oasis_bot):
    oasis_bot.add_cog(NewUserCog(oasis_bot))