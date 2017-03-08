import discord
from discord.ext import commands
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .utils import checks
from .utils.dataIO import fileIO, dataIO
import os
import random


class MMR:
    """Gets MMR for users"""

    def __init__(self, bot):
        self.bot = bot
        self.players = fileIO("data/mmr/players.json", "load")
        self.dotabuff = "https://www.dotabuff.com/players/"

    def get_player_id(self, user: discord.Member):
        data = self.players
        players = data["players"]
        for player in players:
            if user.id == player["discord_id"]:
                return player["dota2_id"]

    @commands.command(pass_context=True)
    async def mmr(self, ctx, user: discord.Member):
        """Shows MMR for user (if registered in file)."""
        dota2_id = self.get_player_id(user)
        if dota2_id is None:
            not_exist = "```\n"
            not_exist += user.display_name
            not_exist += " not registered in file.\n"
            not_exist += "Please use [p]mmradd <user> <dota2_id> to register.\n"
            not_exist += "```"
            await self.bot.say(not_exist)
            return
        url = urljoin(self.dotabuff, dota2_id)
        header = {'User-Agent': 'Friendly Red bot'}
        req = Request(url, headers=header)
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")
        section = soup.findAll("div", {"class": "header-content-secondary"})
        dds = section[0].findAll("dd")
        solo_mmr = dds[1].contents[0]
        party_mmr = dds[2].contents[0]

        if len(solo_mmr) > 4:
            solo_mmr = "TBD"

        if len(party_mmr) > 4:
            party_mmr = "TBD"

        random_color = int("0x%06x" % random.randint(0, 0xFFFFFF), 16)

        embed = discord.Embed(colour=random_color)
        embed.set_author(name=str(user.name))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Solo MMR", value=solo_mmr)
        embed.add_field(name="Party MMR", value=party_mmr)

        await self.bot.say(embed=embed)

    @commands.command(name="mmradd", pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def add_user(self, ctx, user: discord.Member, dota2_id: str):
        """Adds player to file."""
        full_data = self.players
        players = full_data["players"]
        row = {"dota2_id": dota2_id, "discord_id": user.id}
        if not any(player["discord_id"] == user.id for player in players):
            players.append(row)
            fileIO("data/mmr/players.json", "save", full_data)
            await self.bot.say("Player added!")
        else:
            await self.bot.say("Player already exists...")


def check_folder():
    if not os.path.exists("data/mmr"):
        print("Creating mmr folder...")
        os.makedirs("data/mmr")


def check_file():
    contents = {"players": []}
    if not os.path.exists("data/mmr/players.json"):
        print("Creating empty players.json...")
        dataIO.save_json("data/mmr/players.json", contents)


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(MMR(bot))
