import discord
import aiohttp
import os
import random
from discord.ext import commands
from .utils import checks
from .utils.dataIO import fileIO, dataIO


class PUBG:
    """PUBG stats cog"""

    def __init__(self, bot):
        self.bot = bot
        self.api_url = 'https://pubgtracker.com/api/profile/pc/'
        self.config = dataIO.load_json('data/pubg/config.json')
        self.modes = ['solo', 'duo', 'squad']
        self.regions = ['na', 'eu', 'as', 'oc', 'sa', 'agg']

    @commands.group(pass_context=True)
    async def pubg(self, ctx):
        """PUBG Tracker API stats"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.is_owner()
    @pubg.command(no_pm=False, name='tokenset')
    async def _tokenset(self, token: str):
        """Sets token for PUBG Tracker API

        https://pubgtracker.com/site-api"""
        self.config['PUBG_TOKEN'] = token
        dataIO.save_json('data/pubg/config.json', self.config)
        await self.bot.say('PUBG Tracker API token set')

    async def _get_data(self, pubg_nickname: str, category: str, mode: str, region: str):
        if self.config['PUBG_TOKEN'] != '':
            headers = {
                'User-Agent': 'Friendly Red bot',
                'content-type': 'application/json',
                'TRN-Api-Key': self.config['PUBG_TOKEN']
            }
            data = None
            async with aiohttp.get(self.api_url + pubg_nickname, headers=headers) as r:
                data = await r.json()

            filtered_data = None
            for stat in data['Stats']:
                if stat['Match'] == mode and stat['Region'] == region:
                    filtered_data = stat

            categorized_data = {}
            categorized_data['PlayerName'] = data['PlayerName']
            categorized_data['Avatar'] = data['Avatar']
            categorized_data['LastUpdated'] = data['LastUpdated']
            categorized_data['Stats'] = []
            for stat in filtered_data['Stats']:
                if stat['category'] == category:
                    categorized_data['Stats'].append(stat)

            return categorized_data
        else:
            await self.bot.say('Please set your API token via the `[p]pubg tokenset` command')

    @pubg.command(name='performance')
    async def _performance(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets performance stats

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Performance', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Performance'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)

    @pubg.command(name='skillrating')
    async def _skillrating(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets skill rating

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Skill Rating', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Skill Rating'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)

    @pubg.command(name='pergame')
    async def _pergame(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets per game stats

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Per Game', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Per Game'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)

    @pubg.command(name='combat')
    async def _combat(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets combat stats

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Combat', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Combat'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)

    @pubg.command(name='survival')
    async def _survival(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets survival stats

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Survival', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Survival'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)

    @pubg.command(name='distance')
    async def _distance(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets distance stats

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Distance', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Distance'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)

    @pubg.command(name='support')
    async def _support(self, pubg_nickname: str, mode: str='solo', region: str='agg'):
        """Gets support stats

        Available modes are ['solo', 'duo', 'squad'], defaults to: 'solo'
        Available regions are ['na', 'eu', 'as', 'oc', 'sa', 'agg'], defaults to: 'agg' (aggregate)"""
        data = await self._get_data(pubg_nickname, 'Support', mode, region)
        random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_colour)
        embed.title = 'Support'
        embed.set_author(name=data['PlayerName'])
        embed.set_thumbnail(url=data['Avatar'])
        for stat in data['Stats']:
            embed.add_field(name=stat['label'], value=stat['displayValue'])
        embed.set_footer(text='Last updated on ' + data['LastUpdated'])

        await self.bot.say(embed=embed)


def check_folder():
    if not os.path.exists('data/pubg'):
        print('Creating pubg folder...')
        os.makedirs('data/pubg')


def check_file():
    contents = {'PUBG_TOKEN': ''}
    if not os.path.exists('data/pubg/config.json'):
        print('Creating empty config.json')
        dataIO.save_json('data/pubg/config.json', contents)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(PUBG(bot))
