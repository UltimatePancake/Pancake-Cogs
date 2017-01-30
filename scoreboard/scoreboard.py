import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from tabulate import tabulate


class Scoreboard:
    """Dumb little scoreboard cog."""

    def __init__(self, bot):
        self.bot = bot
        self.scoresheet = "data/scoreboard/scoreboard.json"
        self.competition_headers = ["Name", "Created by", "Teams"]
        self.team_headers = ["Name", "Tag", "W", "L", "Players"]
        self.player_headers = ["C", "Player", "Score", "K", "D", "A"]
        self.grid_style = "fancy_grid"

    def get_board(self):
        """Retrieves entire board structure."""
        return fileIO(self.scoresheet, "load")

    def get_competitions(self):
        """Retrieves all competitions."""
        board = self.get_board()
        return board["competitions"]

    def get_single_competition_by_name(self, competition_name: str):
        """Retrieves single competition by name."""
        competitions = self.get_competitions()
        for competition in competitions:
            if competition["name"].lower() == competition_name.lower():
                return competition

    def get_teams(self, competition_name: str):
        """Retrieves all teams in a given competition."""
        competitions = self.get_competitions()
        for competition in competitions:
            if competition["name"].lower() == competition_name.lower():
                return competition["teams"]

    def get_players(self, competition_name: str, team_name: str):
        """Retrieves all players in a team from a given competition."""
        teams = self.get_teams(competition_name)
        for team in teams:
            if team["name"].lower() == team_name.lower():
                return team["players"]

    def get_players_by_tag(self, competition_name: str, team_tag: str):
        """Retrieves all players in a team from a given competition."""
        teams = self.get_teams(competition_name)
        for team in teams:
            if team["tag"].lower() == team_tag.lower():
                return team["players"]

    def get_table(self, data, headers):
        """Generates competition table string."""
        table = "```\n"
        table += tabulate(data, headers, self.grid_style)
        table += "\n```"
        return table

    @commands.group(name="scoreboard", aliases=["scores", "sb"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def scoreboard(self, ctx):
        """Gets scoreboard info."""
        if ctx.invoked_subcommand is None:
            ctx.invoke(self._list_competitions)

    @scoreboard.command(name="listcompetitions", aliases=["lc"], pass_context=True, invoke_without_command=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _list_competitions(self, ctx):
        """Lists current competitions."""
        await self.bot.say("Searching...")
        competitions = self.get_competitions()
        data = []
        for competition in competitions:
            row = [competition["name"], competition["creator"], len(competition["teams"])]
            data.append(row)
        await self.bot.say(self.get_table(data, self.competition_headers))

    @scoreboard.command(name="listteams", aliases=["lt"], pass_context=True, invoke_without_command=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _list_teams(self, ctx, competition_name: str):
        """Lists current teams in competition."""
        await self.bot.say("Searching...")
        teams = self.get_teams(competition_name)
        data = []
        for team in teams:
            row = [team["name"], team["tag"], team["wins"], team["losses"], len(team["players"])]
            data.append(row)
        await self.bot.say(self.get_table(data, self.team_headers))

    @scoreboard.command(name="listplayers", aliases=["lp"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _list_players(self, ctx, competition_name: str, team_name: str):
        """Lists current players in team from given competition."""
        await self.bot.say("Searching...")
        players = self.get_players(competition_name, team_name)
        data = []
        for player in players:
            cap = ""
            if player["is_captain"]:
                cap = "∆"
            row = [cap, player["name"], player["score"], player["kills"], player["deaths"], player["assists"]]
            data.append(row)
        await self.bot.say(self.get_table(data, self.player_headers))

    @scoreboard.command(name="listplayersbytag", aliases=["lpt"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _list_players_by_tag(self, ctx, competition_name: str, team_tag: str):
        """Lists current players in team from given competition."""
        await self.bot.say("Searching...")
        players = self.get_players_by_tag(competition_name, team_tag)
        data = []
        for player in players:
            cap = ""
            if player["is_captain"]:
                cap = "∆"
            row = [cap, player["name"], player["score"], player["kills"], player["deaths"], player["assists"]]
            data.append(row)
        await self.bot.say(self.get_table(data, self.player_headers))

    def add_competition(self, data):
        """Adds a new competition to file."""
        full_data = self.get_board()
        competitions = full_data["competitions"]
        competitions.append(data)
        fileIO(self.scoresheet, "save", full_data)

    def add_team(self, data, competition_name: str):
        """Adds a new team to competition in file."""
        full_data = self.get_board()
        competitions = full_data["competitions"]
        for competition in competitions:
            if competition["name"].lower() == competition_name.lower():
                teams = competition["teams"]
                teams.append(data)
        fileIO(self.scoresheet, "save", full_data)

    def add_player(self, data, competition_name: str, team_name: str):
        """Adds a player to a team in a competition on file."""
        full_data = self.get_board()
        competitions = full_data["competitions"]
        for competition in competitions:
            if competition["name"].lower() == competition_name.lower():
                teams = competition["teams"]
                for team in teams:
                    if team["name"].lower() == team_name.lower():
                        players = team["players"]
                        players.append(data)
        fileIO(self.scoresheet, "save", full_data)

    def add_player_by_tag(self, data, competition_name: str, team_tag: str):
        """Adds a player to a team in a competition on file."""
        full_data = self.get_board()
        competitions = full_data["competitions"]
        for competition in competitions:
            if competition["name"].lower() == competition_name.lower():
                teams = competition["teams"]
                for team in teams:
                    if team["tag"].lower() == team_tag.lower():
                        players = team["players"]
                        players.append(data)
        fileIO(self.scoresheet, "save", full_data)

    @scoreboard.command(name="addcompetition", aliases=["ac", "mkc"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _add_competition(self, ctx, competition_name: str):
        """Adds a new competition to file."""
        new_competition = {
            "name" : competition_name,
            "creator" : ctx.message.author.name,
            "teams" : []
        }
        self.add_competition(new_competition)
        await self.bot.say("Added " + competition_name)

    @scoreboard.command(name="addteam", aliases=["at", "mkt"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _add_team(self, ctx, competition_name: str, team_name: str, team_tag: str=None):
        """Adds a new team to a competition on file."""
        new_team = {
            "name" : team_name,
            "tag" : team_tag,
            "players" : [],
            "wins" : 0,
            "losses" : 0
        }
        self.add_team(new_team, competition_name)
        await self.bot.say("Added " + team_name + " to " + competition_name + "...")

    @scoreboard.command(name="addplayer", aliases=["ap", "mkp"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _add_player(self, ctx, competition_name: str, team_name: str, user: discord.Member, is_captain: bool=False):
        """Adds a player to a team in a competition on file."""
        new_player = {
            "name" : user.name,
            "is_captain" : is_captain,
            "score" : 0,
            "kills" : 0,
            "deaths" : 0,
            "assists" : 0
        }
        self.add_player(new_player, competition_name, team_name)
        await self.bot.say("Added " + user.mention + " to team " + team_name + " in " + competition_name + ".")

    @scoreboard.command(name="addplayerbytag", aliases=["apt", "mkpt"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _add_player_by_tag(self, ctx, competition_name: str, team_tag: str, user: discord.Member, is_captain: bool=False):
        """Adds a player to a team in a competition on file."""
        new_player = {
            "name" : user.name,
            "is_captain" : is_captain,
            "score" : 0,
            "kills" : 0,
            "deaths" : 0,
            "assists" : 0
        }
        self.add_player_by_tag(new_player, competition_name, team_tag)
        await self.bot.say("Added " + user.mention + " to team " + team_tag + " in " + competition_name + ".")

    def clear_scoresheet(self):
        """Removes all competitions and sets a clear sheet."""
        default_data = { "competitions" : [] }
        fileIO(self.scoresheet, "save", default_data)

    @scoreboard.command(name="clearall", aliases=["rmrf"], pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def _clear_all(self):
        """Removes all competitions and sets a clear sheet."""
        self.clear_scoresheet()
        await self.bot.say("Removed everything from scoresheet...")


def setup(bot):
    bot.add_cog(Scoreboard(bot))
