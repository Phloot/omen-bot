import discord
import sys

class OasisBot(discord.Client):
    async def on_ready(self):
        pass

    async def on_disconnect(self):
        try:
            await self.close()
            await sys.exit()
        except Exception as e:
            print("Exception in on_disconnect: {0}".format(str(e)))