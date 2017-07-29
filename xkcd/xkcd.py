"""
    MIT License

    Copyright (c) 2017 Pier-Angelo Gaetani

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import discord
from discord.ext import commands
import xkcd


class XKCD:
    """xkcd comic cog."""

    __author__ = 'UltimatePancake'
    __version__ = '0.1'

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
