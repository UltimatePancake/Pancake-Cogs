import discord
from discord.ext import commands


class dickbutt:
    """Yes, dickbutt."""

    def __init__(self, bot):
        self.bot = bot
        self.image = "data/dickbutt/dickbutt.jpg"

    @commands.command()
    async def dickbutt(self, ctx):
        """Let me reiterate, dickbutt"""

        # code
        channel = ctx.channel
        await self.bot.send_file(channel, self.image)


def setup(bot):
    bot.add_cog(dickbutt(bot))
