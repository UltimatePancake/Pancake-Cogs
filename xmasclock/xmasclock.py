import datetime
import discord
from discord.ext import commands

class xmasclock:
    """I did it!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xmasclock(self):
        """Display days left 'til xmas"""

        #code
        await self.bot.say("I can do stuff!")
        now = datetime.datetime.now()
        await self.bot.say(now.isoformat())


def setup(bot):
    bot.add_cog(xmasclock(bot))
