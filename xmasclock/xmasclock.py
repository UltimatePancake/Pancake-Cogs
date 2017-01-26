import datetime
from datetime import date
import discord
from discord.ext import commands


class xmasclock:
    """I did it!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xmasclock(self):
        """Display days left 'til xmas"""

        now = datetime.datetime.now()
        today = date(now.year, now.month, now.day)
        xmasday = date(now.year, 12, 25)

        delta = xmasday - today

        await self.bot.say(str(delta.days) + " days left until Xmas!")


def setup(bot):
    bot.add_cog(xmasclock(bot))
