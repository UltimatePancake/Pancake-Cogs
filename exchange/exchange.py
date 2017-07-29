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

import aiohttp
from discord.ext import commands

class Exchange:
    """Currency converter"""

    __author__ = 'UltimatePancake'
    __version__ = '0.1'

    def __init__(self, bot):
        self.bot = bot
        self.currencies = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']

    @commands.command()
    async def moneyconvert(self, amount: float, base: str, to: str):
        """Currency converter
        Set the amount, currency FROM (base) and currency TO 
        Available currencies for conversion:
        AUD BGN BRL CAD CHF CNY CZK DKK EUR GBP HKD HRK HUF IDR ILS INR JPY KRW MXN MYR NOK NZD PHP PLN RON RUB SEK SGD THB TRY USD ZAR
        ***WARNING***
        Conversion may not be exact"""
        if base.upper() not in self.currencies or to.upper() not in self.currencies:
            await self.bot.say('One or both of the currencies selected are invalid')
        else:
            api = 'http://api.fixer.io/latest?base={}'.format(base.upper())
            async with aiohttp.request("GET", api) as r:
                result = await r.json()
                rate = result['rates'][to.upper()]
                converted_amount = amount * rate
                pre_conv = '{0:.2f}'.format(amount)
                post_conv = '{0:.2f}'.format(converted_amount)
                await self.bot.say('`{} {} = {} {}`'.format(base.upper(), pre_conv, to.upper(), post_conv))


def setup(bot):
    bot.add_cog(Exchange(bot))
