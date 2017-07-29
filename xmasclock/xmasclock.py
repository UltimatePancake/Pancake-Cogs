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

import datetime
from datetime import date
import discord
from discord.ext import commands


class XmasClock:
    """Simple display of days left until next xmas"""

    __author__ = 'UltimatePancake'
    __version__ = '0.1'

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

        await self.bot.say('```{} days left until Xmas!```'.format(delta.days))


def setup(bot):
    bot.add_cog(XmasClock(bot))
