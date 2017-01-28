import discord
from discord.ext import commands


class Barbaric:
    """Absolutely"""

    def __init__(self, bot):
        self.bot = bot
        self.image = "data/barbaric/barbaric.jpg"

    @commands.command(pass_context=True)
    async def barbaric(self, ctx):
        """Displays dank meme 'absolutely barbaric'"""

        # code
        channel = ctx.message.channel
        await self.bot.send_file(channel, self.image)


def setup(bot):
    n = Barbaric(bot)
    bot.add_cog(n)
