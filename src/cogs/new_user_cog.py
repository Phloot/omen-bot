# src/cogs/new_user_cog.py
from discord.ext import commands

class NewUserCog(commands.Cog):
    def __init__(self, oasis_bot):
        self.oasis_bot = oasis_bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send('Welcome to [CO], {0.mention}! Please check out #role-selection and #community-info when you have time.'.format(member))

def setup(oasis_bot):
    oasis_bot.add_cog(NewUserCog(oasis_bot))