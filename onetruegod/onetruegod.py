import discord
from discord.ext import commands
import random


class OneTrueGod:
    """Everything was Nicolas Cage."""

    def __init__(self, bot):
        self.bot = bot
        self.placecage = "https://www.placecage.com/"

    @commands.command(name="onetruegod", aliases=["cage"])
    async def onetruegod(self):
        """Post random Nicolas Cage image from placecage.com"""

        # code
        w = random.randint(200, 700)
        h = random.randint(200, 700)
        await self.bot.say(self.placecage + str(w) + "/" + str(h))


def setup(bot):
    bot.add_cog(OneTrueGod(bot))
