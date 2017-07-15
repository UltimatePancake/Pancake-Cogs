import discord
from discord.ext import commands

class Dota2Items:
    """Displays information about Dota 2 in-game items"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="itemlist", pass_context=True)
    async def get_item_list(self, ctx):
        await self.bot.say("First")
