from discord.ext import commands
import aiohttp

class DadJokes:
    """Random dad jokes from icanhazdadjoke.com"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self):
        """Gets a random dad joke."""
        api = 'https://icanhazdadjoke.com/'
        async with aiohttp.request('GET', api, headers={'Accept': 'text/plain'}) as r:
            result = await r.text()
            await self.bot.say('`' + result + '`')


def setup(bot):
    n = DadJokes(bot)
    bot.add_cog(n)
