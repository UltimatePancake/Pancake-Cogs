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
import os
from discord.ext import commands
from random import randint
from tabulate import tabulate
from .utils import checks
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box


class Football:
    """Football stats"""

    __author__ = 'UltimatePancake'
    __version__ = '0.2'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = 'http://api.football-data.org/v1/'
        self.config = dataIO.load_json('data/football/config.json')

    async def _make_request(self, url: str, params, server_id: str):
        """The one that actually does the work"""
        headers = {
            'X-Response-Control': 'minified',
            'User-Agent': 'Friendly Red bot'
        }

        if server_id in self.config:
            if 'API_TOKEN' in self.config[server_id]:
                headers['X-Auth-Token'] = self.config['API_TOKEN']
        else:
            await self.bot.say(box('Requests made without an authentication token are limited to 100 requests per 24 hours.\nYou can request a key by registering at http://api.football-data.org and setting it via [p]football tokenset.'))

        async with aiohttp.get(url, headers=headers, params=params) as r:
            # print(vars(r))
            if r.status == 200:
                data = await r.json()
                return data
            elif r.status == 400:
                await self.bot.say(box('Bad Request [400]:\nYour request was malformed most likely the value of a Filter was not set according to the Data Type that is expected.'))
                return
            elif r.status == 403:
                await self.bot.say(box('Restricted Resource [403]:\nYou tried to access a resource that exists, but is not available for you. This can be out of the following reasons:\n- the resource is only available to authenticated clients\n- the resource is only available to donating clients\n- the resource is not available in the API version you are using'))
                return
            elif r.status == 404:
                await self.bot.say(box('Not found [404]\nYou tried to access a resource that doesn’t exist.'))
                return
            elif r.status == 429:
                await self.bot.say(box('Too many requests [429]\nYou exceeded your allowed requests per minute/day depending on API version and your user status.\nSee http://api.football-data.org/docs/v1/index.html#_request_throttling for more information.'))
                await self.bot.say(box('Requests reset in {} seconds.'.format(r.headers['X-RequestCounter-Reset'])))
                return
            else:
                await self.bot.say(box('Pancake has no idea what you\'ve done, seriously.'))
                await self.bot.say(box('{}\n{}'.format(r.status, r.json()['error'])))
                return

    async def _get_full_leagues_data(self, server_id: str, season: str=None):
        """Retrieves all league data from API"""
        if season is None:
            season = ''

        params = { 'season': season }
        url = '{}competitions/'.format(self.api_url)

        return await self._make_request(url, params, server_id)

    async def _get_league_fixtures_timeframe(self, server_id: str, league_id: str, timeframe: str):
        """Retrieves specific league matchday fixtures from API

        Optional timeframe parameter:
        The value of the timeFrame argument must start with either p(ast) or n(ext), representing a timeframe either in the past or future. It is followed by a number in the range 1..99. It defaults to n7 in the fixture resource and is unset for fixture as a subresource.
        For instance: p6 would return all fixtures in the last 6 days, whereas n23 would result in returning all fixtures in the next 23 days."""
        params = { 'timeFrame': timeframe }
        url = '{}competitions/{}/fixtures'.format(self.api_url, league_id)

        return await self._make_request(url, params, server_id)

    async def _get_league_fixtures_matchday(self, server_id: str, league_id: str, matchday: str):
        """Retrieves specific league matchday fixtures from API"""
        params = { 'matchday': matchday }
        url = '{}competitions/{}/fixtures'.format(self.api_url, league_id)

        return await self._make_request(url, params, server_id)

    async def _get_league_leaderboard(self, server_id: str, league_id: str, timeframe: str):
        """Retrieves specific league leaderboard from API

        Optional timeframe parameter:
        The value of the timeFrame argument must start with either p(ast) or n(ext), representing a timeframe either in the past or future. It is followed by a number in the range 1..99. It defaults to n7 in the fixture resource and is unset for fixture as a subresource.
        For instance: p6 would return all fixtures in the last 6 days, whereas n23 would result in returning all fixtures in the next 23 days."""
        params = { 'timeFrame': timeframe }
        url = '{}competitions/{}/leagueTable'.format(self.api_url, league_id)

        return await self._make_request(url, params, server_id)

    async def _get_team_info(self, server_id: str, team_id: str):
        """Retrieves specific team info"""
        params = {}
        url = '{}teams/{}'.format(self.api_url, team_id)

        return await self._make_request(url, params, server_id)

    async def _get_team_players(self, server_id: str, team_id: str):
        """Retrieves specific team players"""
        params = {}
        url = '{}teams/{}/players'.format(self.api_url, team_id)

        return await self._make_request(url, params, server_id)

    @commands.group(pass_context=True)
    async def football(self, ctx: commands.Context):
        """Gets league/team standings and stats"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @checks.admin_or_permissions(manage_server=True)
    @football.command(name='tokenset', pass_context=True)
    async def _tokenset(self, ctx: commands.Context, token: str):
        """Sets token for football-data.org API
        http://api.football-data.org/client/register"""
        self.config[ctx.message.server.id] = token
        dataIO.save_json('data/football/config.json', self.config)
        await self.bot.say('football-data API token set')

    @football.command(name='leagues', pass_context=True)
    async def _leagues(self, ctx: commands.Context, season: str=None):
        """Gets leagues info"""
        headers = ['League', 'id', 'Name', 'Teams', 'Games', 'Matchdays']
        data = await self._get_full_leagues_data(ctx.message.server.id, season)
        pretty_data = []

        for league in data:
            pretty_data.append([league['league'], league['id'], league['caption'], league['numberOfTeams'], league['numberOfGames'], league['numberOfMatchdays']])

        await self.bot.say(box(tabulate(pretty_data, headers=headers)))

    @football.command(name='leaderboard', pass_context=True)
    async def _leaderboard(self, ctx: commands.Context, league_id: str, matchday: str=None):
        """Gets league leaderboard"""
        headers = [' ', 'ID', 'Team', 'Points', 'P', 'G', 'GA', 'GD']
        data = await self._get_league_leaderboard(ctx.message.server.id, league_id, matchday)
        pretty_data = []

        await self.bot.say('```diff\n+ {}\n- Matchday: {}\n```'.format(data['leagueCaption'], data['matchday']))

        if 'standing' in data:
            for team in data['standing']:
                pretty_data.append([team['rank'], team['teamId'], team['team'], team['points'], team['playedGames'], team['goals'], team['goalsAgainst'], team['goalDifference']])

            await self.bot.say(box(tabulate(pretty_data, headers=headers)))
        elif 'standings' in data:
            for group, v in data['standings'].items():
                asyncio.sleep(1)
                await self.bot.say('```diff\n+ Group {}```'.format(group))
                pretty_data = []

                for team in v:
                    pretty_data.append([team['rank'], team['team'], team['points'], team['playedGames'], team['goals'], team['goalsAgainst'], team['goalDifference']])

                await self.bot.say(box(tabulate(pretty_data, headers=headers)))

    @football.group(pass_context=True)
    async def fixtures(self, ctx: commands.Context):
        """Fixture commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @fixtures.command(name='last', pass_context=True)
    async def _lastfixtures(self, ctx: commands.Context, league_id: str):
        """Gets last matchday fixtures"""
        headers = ['ID', 'Home', 'G', ' ' , 'G', 'Away']
        data = await self._get_league_fixtures_timeframe(ctx.message.server.id, league_id, 'p7')

        await self.bot.say('```diff\n+ Last fixtures```')
        pretty_data = []
        for fixture in data['fixtures']:
            pretty_data.append([
                fixture['id'],
                '[{}] {}'.format(fixture['homeTeamId'], fixture['homeTeamName']),
                fixture['goalsHomeTeam'],
                ' - ',
                fixture['goalsAwayTeam'],
                '[{}] {}'.format(fixture['awayTeamId'], fixture['awayTeamName'])
            ])

        await self.bot.say(box(tabulate(pretty_data, headers=headers)))

    @fixtures.command(name='next', pass_context=True)
    async def _nextfixtures(self, ctx: commands.Context, league_id: str):
        """Gets last matchday fixtures"""
        headers = ['ID', 'Home', ' ' , 'Away', 'Date']
        data = await self._get_league_fixtures_timeframe(ctx.message.server.id, league_id, 'n7')

        await self.bot.say('```diff\n+ Next fixtures```')
        pretty_data = []
        for fixture in data['fixtures']:
            pretty_data.append([
                fixture['id'],
                '[{}] {}'.format(fixture['homeTeamId'], fixture['homeTeamName']),
                ' - ',
                '[{}] {}'.format(fixture['awayTeamId'], fixture['awayTeamName']),
                fixture['date']
            ])

        await self.bot.say(box(tabulate(pretty_data, headers=headers)))

    @fixtures.command(name='matchday', pass_context=True)
    async def _matchdayfixtures(self, ctx: commands.Context, league_id: str, matchday: str='1'):
        """Gets specific matchday fixtures

        Defaults to matchday 1"""
        headers = ['ID', 'Home', ' ', ' ' , 'Away']
        data = await self._get_league_fixtures_matchday(ctx.message.server.id, league_id, matchday)

        await self.bot.say('```diff\n+ Matchday {} fixtures```'.format(matchday))
        pretty_data = []
        for fixture in data['fixtures']:
            pretty_data.append([
                fixture['id'],
                '[{}] {}'.format(fixture['homeTeamId'], fixture['homeTeamName']),
                fixture['result']['goalsHomeTeam'],
                fixture['result']['goalsAwayTeam'],
                '[{}] {}'.format(fixture['awayTeamId'], fixture['awayTeamName'])
            ])

        await self.bot.say(box(tabulate(pretty_data, headers=headers)))

    @football.command(pass_context=True)
    async def team(self, ctx: commands.Context, team_id: str=None, show_players: bool=True):
        """Gets team information"""
        if team_id is None:
            await self.bot.send_cmd_help(ctx)
        else:
            team_data = await self._get_team_info(ctx.message.server.id, team_id)
            embed = discord.Embed(colour=randint(0, 0xFFFFFF))
            embed.title = team_data['name']
            if team_data['squadMarketValue'] is not None:
                embed.add_field(name='Squad market value', value=team_data['squadMarketValue'])

            embed.set_thumbnail(url=team_data['crestUrl'].replace('http', 'https'))
            embed.set_footer(text='id: {}'.format(team_id))
            await self.bot.say(embed=embed)

            if show_players:
                team_players = await self._get_team_players(ctx.message.server.id, team_id)
                await self.bot.say('```diff\n+ {} roster```'.format(team_data['name']))
                headers = ['Name', 'Jersey', 'Nationality', 'DoB', 'Position', 'Contract']
                pretty_data = []
                for player in team_players['players']:
                    pretty_data.append([
                        player['name'],
                        player['jerseyNumber'],
                        player['nationality'],
                        player['dateOfBirth'],
                        player['position'],
                        player['contractUntil']
                    ])

                for page in pagify(tabulate(pretty_data, headers=headers), ['\n'], shorten_by=8):
                    await self.bot.say(box(page))


def check_folder():
    if not os.path.exists('data/football'):
        print('Creating pubg folder...')
        os.makedirs('data/football')


def check_file():
    contents = {}
    if not os.path.exists('data/football/config.json'):
        print('Creating empty config.json')
        dataIO.save_json('data/football/config.json', contents)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Football(bot))
