# src/cogs/new_user_cog.py
from discord.ext import commands
from functions import return_config

class NewUserCog(commands.Cog):
    def __init__(self, oasis_bot):
        self.oasis_bot = oasis_bot
        self.configs = return_config()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send('Welcome to [CO], {0.mention}! Please check out {1.mention} and {2.mention} when you have time.'.format
            (
                member,
                self.configs['discord_channels']['role_selection'],
                self.configs['discord_channels']['community_info'],
                )
            )

def setup(oasis_bot):
    oasis_bot.add_cog(NewUserCog(oasis_bot))