import discord
from discord.ext import commands


class dickbutt:
    """Yes, dickbutt."""

    def __init__(self, bot):
        self.bot = bot
        self.image = "data/dickbutt/dickbutt.jpg"

    @commands.command()
    async def dickbutt(self):
        """Let me reiterate, dickbutt"""

        # code
        # channel = ctx.message.channel
        await self.bot.send_file(self.image)


def setup(bot):
    bot.add_cog(dickbutt(bot))
