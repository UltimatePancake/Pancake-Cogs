import discord
from discord.ext import commands
import random


class onetruegod:
    """Everything was Nicolas Cage."""

    def __init__(self, bot):
        self.bot = bot
        self.placecage = "https://www.placecage.com/"

    @commands.command()
    async def onetruegod(self):
        """And nothing hurt..."""

        # code
        w = random.randint(200, 700)
        h = random.randint(200, 700)
        await self.bot.say(self.placecage + str(w) + "/" + str(h))


def setup(bot):
    bot.add_cog(onetruegod(bot))
