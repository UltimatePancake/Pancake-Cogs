import discord
from discord.ext import commands
import xkcd


class XKCD:
    """xkcd comic cog."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="xkcd", pass_context=True)
    async def xkcd(self, ctx):
        """Displays latest xkcd comic."""
        if ctx.invoked_subcommand is None:
            await self.bot.say(xkcd.getLatestComic().getImageLink())

    @xkcd.command(name="random", pass_context=True)
    async def _random(self, ctx):
        """Displays random xkcd comic."""
        await self.bot.say(xkcd.getRandomComic().getImageLink())

    @xkcd.command(name="number", pass_context=True)
    async def _number(self, ctx, number: int):
        """Displays specified xkcd comic."""
        await self.bot.say(xkcd.getComic(number).getImageLink())


def setup(bot):
    bot.add_cog(XKCD(bot))
