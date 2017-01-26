import discord
from discord.ext import commands


class dickbutt:
    """Yes, dickbutt."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dickbutt(self, ctx):
        """Let me reiterate, dickbutt"""

        # code
        image = "data/dickbutt/dickbutt.jpg"
        channel = ctx.message.channel
        await self.bot.send_file(channel, image)


def setup(bot):
    bot.add_cog(dickbutt(bot))
