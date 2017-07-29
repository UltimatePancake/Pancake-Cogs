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
from discord.ext import commands
from bs4 import BeautifulSoup
from random import randint
from .utils import checks
from .utils.dataIO import dataIO
import os
import aiohttp


class MMR:
    """Gets MMR for users"""

    __author__ = 'UltimatePancake'
    __version__ = '0.1'

    def __init__(self, bot):
        self.bot = bot
        self.players = dataIO.load_json('data/mmr/players.json')
        self.dotabuff = 'https://www.dotabuff.com/players/'

    def get_player_id(self, user: discord.Member):
        data = self.players
        players = data['players']
        for player in players:
            if user.id == player['discord_id']:
                return player['dota2_id']

    @commands.command(pass_context=True)
    async def mmr(self, ctx, user: discord.Member):
        """Shows MMR for user (if registered in file)."""
        dota2_id = self.get_player_id(user)
        if dota2_id is None:
            not_exist = '```\n'
            not_exist += user.display_name
            not_exist += ' not registered in file.\n'
            not_exist += 'Please use [p]mmradd <user> <dota2_id> to register.\n'
            not_exist += '```'
            await self.bot.say(not_exist)
            return

        url = self.dotabuff + dota2_id
        header = {'User-Agent': 'Friendly Red bot'}

        async with aiohttp.get(url, headers=header) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')

        section = soup.findAll('div', {'class': 'header-content-secondary'})
        dds = section[0].findAll('dd')
        solo_mmr = dds[1].contents[0]
        party_mmr = dds[2].contents[0]

        if len(solo_mmr) > 4:
            solo_mmr = 'TBD'

        if len(party_mmr) > 4:
            party_mmr = 'TBD'

        embed = discord.Embed(colour=randint(0, 0xFFFFFF))
        embed.set_author(name=str(user.name))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Solo MMR', value=solo_mmr)
        embed.add_field(name='Party MMR', value=party_mmr)
        embed.set_footer(text='id {}'.format(dota2_id), icon_url='http://cache1.www.gametracker.com/images/game_icons16/dota2.png')
        embed.url = url

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def records(self, ctx, user: discord.Member):
        """Shows Records for user (if registered in file)."""
        dota2_id = self.get_player_id(user)
        if dota2_id is None:
            not_exist = '```\n'
            not_exist += user.display_name
            not_exist += ' not registered in file.\n'
            not_exist += 'Please use [p]mmradd <user> <dota2_id> to register.\n'
            not_exist += '```'
            await self.bot.say(not_exist)
            return

        url = self.dotabuff + dota2_id + '/records'
        header = {'User-Agent': 'Friendly Red bot'}

        async with aiohttp.get(url, headers=header) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')

        section = soup.findAll('div', {'class': 'card'})
        records = {}

        for record in section:
            k = record.find('div', {'class': 'title'}).contents[0]
            v = record.find('div', {'class': 'value'}).contents[0]
            h = record.find('div', {'class': 'hero'}).contents[0]
            records[k] = { 'value' : v, 'hero' : h }

        embed = discord.Embed(colour=randint(0, 0xFFFFFF))
        embed.set_author(name=str(user.name))
        embed.set_thumbnail(url=user.avatar_url)

        for k, v in records.items():
            hero = v['hero'].split('  ')
            embed.add_field(name=k, value='{}\n{}'.format(hero[0], v['value']))

        embed.set_footer(text='id {}'.format(dota2_id), icon_url='http://cache1.www.gametracker.com/images/game_icons16/dota2.png')
        embed.url = url

        await self.bot.say(embed=embed)

    @commands.command(name='mmradd', pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def add_user(self, ctx, user: discord.Member, dota2_id: str):
        """Adds player to file."""
        full_data = self.players
        players = full_data['players']
        row = {'dota2_id': dota2_id, 'discord_id': user.id}
        if not any(player['discord_id'] == user.id for player in players):
            players.append(row)
            dataIO.save_json('data/mmr/players.json', full_data)
            await self.bot.say('Player added!')
        else:
            await self.bot.say('Player already exists, use [p]mmrupdate to update user info.')

    @commands.command(name='mmrupdate', pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def update_user(self, ctx, user: discord.Member, dota2_id: str):
        """Updates player in file."""
        full_data = self.players
        players = full_data['players']
        row = {'dota2_id': dota2_id, 'discord_id': user.id}
        for player in players:
            if player['discord_id'] == user.id:
                players.remove(player)
                players.append(row)
                dataIO.save_json('data/mmr/players.json', full_data)
                await self.bot.say('Player updated!')


def check_folder():
    if not os.path.exists('data/mmr'):
        print('Creating mmr folder...')
        os.makedirs('data/mmr')


def check_file():
    contents = {'players': []}
    if not os.path.exists('data/mmr/players.json'):
        print('Creating empty players.json...')
        dataIO.save_json('data/mmr/players.json', contents)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(MMR(bot))
