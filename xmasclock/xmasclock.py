import datetime
from datetime import date
import discord
from discord.ext import commands


class XmasClock:
    """Simple display of days left until next xmas"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xmasclock(self):
        """Display days left 'til xmas"""

        now = datetime.datetime.now()
        today = date(now.year, now.month, now.day)

        year = now.year
        if (now.month == 12 and now.day > 25):
            year = now.year + 1

        xmasday = date(year, 12, 25)

        delta = xmasday - today

        await self.bot.say("```" + str(delta.days) + " days left until Xmas!```")


def setup(bot):
    bot.add_cog(XmasClock(bot))
