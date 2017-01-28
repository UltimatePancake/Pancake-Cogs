import discord


class richie:
    """Is it me you're looking for?"""

    def __init__(self, bot):
        self.bot = bot
        self.message = "Is it me you're looking for?"

    async def listener(self, message):
        if message.author.id != self.bot.user.id:
            if message.content.lower().startswith('hello'):
                await self.bot.send_message(message.channel, self.message)


def setup(bot):
    n = richie(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)
