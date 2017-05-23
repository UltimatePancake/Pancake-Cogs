import aiohttp
from discord.ext import commands

class Exchange:
    """Currency converter"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def moneyconvert(self, amount: float, base: str, to: str):
        """Currency converter
        Set the amount, currency TO and currency FROM
        Available currencies for conversion:
        AUD BGN BRL CAD CHF CNY CZK DKK EUR GBP HKD HRK HUF IDR ILS INR JPY KRW MXN MYR NOK NZD PHP PLN RON RUB SEK SGD THB TRY USD ZAR
        ***WARNING***
        Conversion may not be exact"""
        api = 'http://api.fixer.io/latest?base={}'.format(base)
        async with aiohttp.request("GET", api) as r:
            result = await r.json()
            rate = result['rates'][to]
            converted_amount = amount * rate
            pre_conv = '{0:.2f}'.format(amount)
            post_conv = '{0:.2f}'.format(converted_amount)
            await self.bot.say('`' + base + ' ' + pre_conv + ' = ' + to + ' ' + post_conv + '`')


def setup(bot):
    bot.add_cog(Exchange(bot))
