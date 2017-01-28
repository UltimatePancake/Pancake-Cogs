import discord


class Richie:
    """Responds to 'hello' by quoting the hit 1984 song 'Hello' by Lionel Richie"""

    def __init__(self, bot):
        self.bot = bot
        self.message = "Is it me you're looking for?"

    async def listener(self, message):
        if message.author.id != self.bot.user.id:
            if message.content.lower().startswith('hello'):
                await self.bot.send_message(message.channel, self.message)


def setup(bot):
    n = Richie(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)
