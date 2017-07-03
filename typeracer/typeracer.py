import discord
import aiohttp
import random
from discord.ext import commands


class TypeRacer:
    """Typeracer stats"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def typeracer(self, user: str):
        """Get user stats from typeracer API"""
        api = 'http://data.typeracer.com/users?id=tr:{}'.format(user)
        async with aiohttp.request("GET", api) as r:
            if r.status == 200:
                result = await r.json()

                random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

                last_scores = '\n'.join(str(int(x)) for x in result['tstats']['recentScores'])

                embed = discord.Embed(colour=random_colour)
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
                await self.bot.say('`Unable to retieve stats for user ' + user + '`')


def setup(bot):
    bot.add_cog(TypeRacer(bot))
