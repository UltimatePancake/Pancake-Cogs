import discord
from discord.ext import commands

class xmasclock:
    """I did it!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xmasclock(self):
        """This does stuff!"""

        #code
        await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(xmasclock(bot))
