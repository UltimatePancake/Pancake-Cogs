import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import xml.etree.ElementTree as Et


class Scoreboard:
    """Dumb little scoreboard cog."""

    def __init__(self, bot):
        self.bot = bot

    def get_board(self):
        return Et.parse("data/scoreboard/scoreboard.xml")

    def get_competitions(self):
        board = self.get_board()
        competitions = board.getroot()
        return competitions

    def get_teams(self, competition: str):
        board = self.get_board()
        teams = board.findall(".//*[@name=\'" + competition + "\']/teams/team")
        return teams

    def get_players(self, competition: str, team: str):
        board = self.get_board()
        players = board.findall(".//*[@name=\'" + competition + "\']/teams/*[@name=\'" + team + "\']/players/player")
        return players

    @commands.group(name="scoreboard", aliases=["scores", "sb"], pass_context=True)
    async def scoreboard(self, ctx):
        """Gets scoreboard info."""

    @scoreboard.command(name="listcompetitions", aliases=["lsc"], pass_context=True)
    async def _listcompetitions(self, ctx):
        """Lists current competitions."""
        competition_list = "**Competitions currently on file:**\n\n    "
        for competition in self.get_competitions():
            competition_list += competition.attrib.get("name") + "\n    "
        await self.bot.say(competition_list)

    @scoreboard.command(name="addcompetition", aliases=["mkc"], pass_context=True)
    async def _addcompetition(self, ctx, competition):
        """Adds a new competition."""

    @scoreboard.command(name="removecompetition", aliases=["rmc"], pass_context=True)
    async def _removecompetition(self, ctx, competition):
        """Removes a competition."""

    @scoreboard.command(name="listteams", aliases=["lst"], pass_context=True)
    async def _listteams(self, ctx, competition: str):
        """Lists teams in competition."""
        team_list = "**Teams currently in \'" + competition + "\':**\n\n    "
        for team in self.get_teams(competition):
            team_list += team.attrib.get("name") + "\n    "
        await self.bot.say(team_list)

    @scoreboard.command(name="addteam", aliases=["mkt"], pass_context=True)
    async def _addteam(self, ctx, competition, team):
        """Adds team to competition."""

    @scoreboard.command(name="removeteam", aliases=["rmt"], pass_context=True)
    async def _removeteam(self, ctx, competition, team):
        """Removes team from competition."""

    @scoreboard.command(name="listplayers", aliases=["lsp"], pass_context=True)
    async def _listplayers(self, ctx, competition, team):
        """Lists players in team from competition"""
        player_list = "**Players currently in \'" + competition + "\', team \'" + team + "\':**\n\n    "
        for player in self.get_players(competition, team):
            if player.attrib.get("iscaptain") == "True":
                player_list += "=C= "
            player_list += player.attrib.get("id") + "\n    "
        await self.bot.say(player_list)

    @scoreboard.command(name="addplayer", aliases=["mkp"], pass_context=True)
    async def _addplayer(self, ctx, competition, team, player):
        """Adds player to team from competition"""

    @scoreboard.command(name="removeplayer", aliases=["rmp"], pass_context=True)
    async def _removeplayer(self, ctx, competition, team, player):
        """Removes player from team from competition"""


def setup(bot):
    bot.add_cog(Scoreboard(bot))
