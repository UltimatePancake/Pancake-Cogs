import discord
from discord.ext import commands
from challonge import set_credentials, tournaments, matches, participants
from .utils.dataIO import dataIO
from .utils import checks
from tabulate import tabulate
import os
import random
import urllib

class Challonge:
    """Sweet hitch-hiker"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/challonge/settings.json")
        if "user" in self.settings and "key" in self.settings:
            self.set_key()

    def set_key(self):
        set_credentials(self.settings["user"], self.settings["key"])
        print("Challonge API credentials set for user " + self.settings["user"] + ".")

    @commands.group(name="challonge", pass_context=True)
    async def challonge(self, ctx: commands.context.Context):
        """Arena of pleasure"""
        if ctx.invoked_subcommand is None:
            print(type(self.bot))

    @challonge.command(name="keyset")
    @checks.is_owner()
    async def _keyset(self, user: str, key: str):
        """Return trip"""
        self.settings["user"] = user
        self.settings["key"] = key
        dataIO.save_json("data/challonge/settings.json", self.settings)
        self.set_key()
        await self.bot.say("API key set.")

    @challonge.command(name="listtournaments")
    async def _listtournaments(self):
        """So nail the hearts"""
        headers = ["Name", "ID", "Game", "Participants", "Tournament type", "State"]
        table = []
        for t in tournaments.index():
            if t["state"] == "underway" or t["state"] == "pending":
                table.append([t["name"], t["id"], t["game-name"], t["participants-count"], t["tournament-type"], t["state"]])
        result = "```\n"
        result += tabulate(table, headers)
        result += "\n```"
        await self.bot.say(result)

    @challonge.command(name="tournament")
    async def _tournament(self, id: int):
        """Ancient vampires"""
        for t in tournaments.index():
            if t["id"] == id:
                random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)
                embed = discord.Embed(colour=random_colour)
                embed.set_image(url=t["live-image-url"])
                embed.set_thumbnail(url=t["live-image-url"])
                embed.url = t["full-challonge-url"]
                embed.title = t["name"]
                embed.add_field(name="Tournament format", value=t["tournament-type"].title())
                embed.add_field(name="Participants", value=t["participants-count"])
                embed.set_footer(text="ID: " + str(t["id"]))

                await self.bot.say(embed=embed)

    @challonge.command(name="showT")
    async def _showtournament(self, id: int):
        """Retrieve a single tournament record"""
        try:
            t = tournaments.show(id)
            random_colour = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)
            embed = discord.Embed(colour=random_colour)
            embed.set_image(url=t["live-image-url"])
            embed.set_thumbnail(url=t["live-image-url"])
            embed.url = t["full-challonge-url"]
            embed.title = t["name"]
            embed.add_field(name="Tournament format", value=t["tournament-type"].title())
            embed.add_field(name="Participants", value=t["participants-count"])
            embed.add_field(name="Progress", value=get_progress_bar(t["progress-meter"]))
            embed.set_footer(text="ID: " + str(t["id"]))
            await self.bot.say(embed=embed)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                await self.bot.say("Tournament with Id: {} not found".format(id))



    @challonge.command(name="createtournament")
    async def _createtournament(self, name: str, url: str, format: str="single elimination"):
        """Repentless
        Formats available: 'single elimination', 'double elmination', 'round robin', 'swiss'"""
        tournaments.create(name, url, format)
        await self.bot.say("Tournament created!")

    @challonge.command(name="deletetournament")
    async def _deletetournament(self, tournament: int):
        """Il vampiro"""
        for t in tournaments.index():
            if t["id"] == tournament:
                await self.bot.say("Tournament " + t["name"] + "with id " + t["id"] + "has been deleted.")
                tournaments.destroy(t["id"])

    @challonge.command(name="starttournament")
    async def _starttournament(self, tournament: int):
        """Woods of Valacchia"""
        for t in tournaments.index():
            if t["id"] == tournament:
                tournaments.start(tournament)
                await self.bot.say(t["name"] + " started!")

    @challonge.command(name="resettournament")
    async def _resettournament(self, tournament: int):
        """When the wolves cry"""
        for t in tournaments.index():
            if t["id"] == tournament:
                tournaments.reset(tournament)
                await self.bot.say(t["name"] + " reset!")

    @challonge.command(name="jointournament", pass_context=True)
    async def _jointournament(self, ctx, tournament: int):
        """Exorcism"""
        for t in tournaments.index():
            if t["id"] == tournament:
                participants.create(tournament, ctx.message.author.id)
                await self.bot.say(ctx.message.author.mention + ", you've been added to tournament " + str(tournament) + ".")

    @challonge.command(name="addparticipant")
    async def _addparticipant(self, tournament: int, user: discord.User):
        """Enthrone the dark angel"""
        for t in tournaments.index():
            if t["id"] == tournament:
                participants.create(tournament, user.id)
                await self.bot.say("User " + user.mention + " has been added to tournament " + str(tournament) + ".")


def get_progress_bar(progress):

    totalP = 100
    barP = 50
    filledP = int(round(barP * progress / float(totalP)))
    percentP = round(100.0 * progress / float(totalP), 1)
    bar = str(progress)+"%" + "[" + ('#' * filledP) + '-' * (barP - filledP)+"]"
    return bar

def check_folder():
    if not os.path.exists("data/challonge"):
        print("Creating challonge folder...")
        os.makedirs("data/challonge")


def check_file():
    contents = {}
    if not os.path.exists("data/challonge/settings.json"):
        print("Creating empty settings.json...")
        dataIO.save_json("data/challonge/settings.json", contents)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Challonge(bot))
