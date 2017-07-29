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

from discord.ext import commands


class Dank:
    """Dank memes, yo."""

    def __init__(self, bot):
        self.bot = bot
        self.base = "data/dank/"

    @commands.command(pass_context=True)
    async def dickbutt(self, ctx):
        """Dickbutt."""
        await self.bot.send_file(ctx.message.channel, "{}dickbutt.png".format(self.base))

    @commands.command(pass_context=True)
    async def barbaric(self, ctx):
        """Absolutely."""
        await self.bot.send_file(ctx.message.channel, "{}barbaric.jpg".format(self.base))

    @commands.command(pass_context=True)
    async def pathetic(self, ctx):
        """Pathetic."""
        await self.bot.send_file(ctx.message.channel, "{}pathetic.png".format(self.base))

    @commands.command(pass_context=True)
    async def snoop(self, ctx):
        """Snoop loves ya too."""
        await self.bot.send_file(ctx.message.channel, "{}snoop.jpg".format(self.base))


def setup(bot):
    bot.add_cog(Dank(bot))
