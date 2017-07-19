import discord
from discord.ext import commands
# from .utils.dataIO import fileIO
from PyDictionary import PyDictionary


class Dictionary:
    """Word, yo"""

    def __init__(self, bot):
        self.bot = bot
        self.dictionary = PyDictionary()
        # self.lang = fileIO("data/dictionary/lang.json", "load")

    @commands.command(name="define", pass_context=True)
    async def define(self, ctx, *, word: str):
        """Displays definitions of a given word"""
        # TODO: Figure out why some values get cut off
        x = await self.bot.say("Searching...")
        search_term = word.split(" ", 1)[0]
        result = self.dictionary.meaning(search_term)
        str_buffer = ""
        if result is None:
            await self.bot.delete_message(x)
            await self.bot.say("This word is not in the dictionary.")
            return
        for key in result:
            str_buffer += "\n**" + key + "**: \n"
            counter = 1
            j = False
            for val in result[key]:
                if val.startswith("("):
                    str_buffer += str(counter) + ". *" + val + ")* "
                    counter += 1
                    j = True
                else:
                    if j:
                        str_buffer += val + "\n"
                        j = False
                    else:
                        str_buffer += str(counter) + ". " + val + "\n"
                        counter += 1
        print(str_buffer)
        await self.bot.delete_message(x)
        await self.bot.say(str_buffer)

    @commands.command(name="antonym", pass_context=True)
    async def antonym(self, ctx, *, word: str):
        """Displays antonyms for a given word"""
        x = await self.bot.say("Searching...")
        search_term = word.split(" ", 1)[0]
        result = self.dictionary.antonym(search_term)
        await self.bot.delete_message(x)
        await self.bot.say("Antonyms for **" + search_term + "**: *" + "*, *".join(result) + "*")

    @commands.command(name="synonym", pass_context=True)
    async def synonym(self, ctx, *, word: str):
        """Displays synonyms for a given word"""
        x = await self.bot.say("Searching...")
        search_term = word.split(" ", 1)[0]
        result = self.dictionary.synonym(search_term)
        await self.bot.delete_message(x)
        await self.bot.say("Synonyms for **" + search_term + "**: *" + "*, *".join(result) + "*")

    # TODO: find a fix for the 400 error when trying to translate
    # @commands.command(name="translate", pass_context=True)
    # async def translate(self, ctx, word: str, to_language: str):
    #     """Displays translation for a given word in a given language"""
    #     TODO: create .json with available gtranslate languages and keys
    #     TODO: search for lang keys in lang.json using friendly terms (english, spanish instead of en, es)
    #     await self.bot.say("Searching...")
    #     search_term = word
    #     lang = to_language
    #     result = self.dictionary.translate(search_term, lang)
    #     await self.bot.say(result)


def setup(bot):
    bot.add_cog(Dictionary(bot))
