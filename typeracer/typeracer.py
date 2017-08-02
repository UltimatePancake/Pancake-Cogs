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
import aiohttp
from random import randint
from discord.ext import commands


class TypeRacer:
    """Typeracer stats"""

    __author__ = 'UltimatePancake'
    __version__ = '0.1'

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def typeracer(self, user: str):
        """Get user stats from typeracer API"""
        api = 'http://data.typeracer.com/users?id=tr:{}'.format(user)
        async with aiohttp.request("GET", api) as r:
            if r.status == 200:
                result = await r.json()

                last_scores = '\n'.join(str(int(x)) for x in result['tstats']['recentScores'])

                embed = discord.Embed(colour=randint(0, 0xFFFFFF))
                embed.set_author(name=result['name'])
                embed.add_field(name='Country', value=':flag_{}:'.format(result['country']))
                embed.add_field(name='Level', value=result['tstats']['level'])
                embed.add_field(name='Wins', value=result['tstats']['gamesWon'])
                embed.add_field(name='Recent WPM', value=int(result['tstats']['recentAvgWpm']))
                embed.add_field(name='Average WPM', value=int(result['tstats']['wpm']))
                embed.add_field(name='Best WPM', value=int(result['tstats']['bestGameWpm']))
                embed.add_field(name='Recent scores', value=last_scores)
                embed.set_footer(text='typeracer.com')
                embed.url = 'http://play.typeracer.com/'

                await self.bot.say(embed=embed)
            else:
                await self.bot.say('`Unable to retrieve stats for user {}`'.format(user))


def setup(bot):
    bot.add_cog(TypeRacer(bot))
