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
# from .utils.dataIO import fileIO
from PyDictionary import PyDictionary


class Dictionary:
    """Word, yo"""

    __author__ = 'UltimatePancake'
    __version__ = '0.3'

    def __init__(self, bot):
        self.bot = bot
        self.dictionary = PyDictionary()
        # self.lang = fileIO('data/dictionary/lang.json', 'load')

    @commands.command(name='define', pass_context=True)
    async def define(self, ctx, *, word: str):
        """Displays definitions of a given word"""
        # TODO: Figure out why some values get cut off
        x = await self.bot.say('Searching...')
        search_term = word.split(' ', 1)[0]
        result = self.dictionary.meaning(search_term)
        str_buffer = ''
        if result is None:
            await self.bot.delete_message(x)
            await self.bot.say('This word is not in the dictionary.')
            return
        for key in result:
            str_buffer += '\n**{}**: \n'.format(key)
            counter = 1
            j = False
            for val in result[key]:
                if val.startswith('('):
                    str_buffer += '{}. *{})* '.format(counter, val)
                    counter += 1
                    j = True
                else:
                    if j:
                        str_buffer += '{}\n'.format(val)
                        j = False
                    else:
                        str_buffer += '{}. {}\n'.format(counter, val)
                        counter += 1
        print(str_buffer)
        await self.bot.delete_message(x)
        await self.bot.say(str_buffer)

    @commands.command(name='antonym', pass_context=True)
    async def antonym(self, ctx, *, word: str):
        """Displays antonyms for a given word"""
        x = await self.bot.say('Searching...')
        search_term = word.split(' ', 1)[0]
        result = self.dictionary.antonym(search_term)
        await self.bot.delete_message(x)
        await self.bot.say('Antonyms for **{}**: *{}*'.format(search_term, '*, *'.join(result)))

    @commands.command(name='synonym', pass_context=True)
    async def synonym(self, ctx, *, word: str):
        """Displays synonyms for a given word"""
        x = await self.bot.say('Searching...')
        search_term = word.split(' ', 1)[0]
        result = self.dictionary.synonym(search_term)
        await self.bot.delete_message(x)
        await self.bot.say('Synonyms for **{}**: *{}*'.format(search_term, '*, *'.join(result)))

    # TODO: find a fix for the 400 error when trying to translate
    # @commands.command(name='translate', pass_context=True)
    # async def translate(self, ctx, word: str, to_language: str):
    #     """Displays translation for a given word in a given language"""
    #     TODO: create .json with available gtranslate languages and keys
    #     TODO: search for lang keys in lang.json using friendly terms (english, spanish instead of en, es)
    #     await self.bot.say('Searching...')
    #     search_term = word
    #     lang = to_language
    #     result = self.dictionary.translate(search_term, lang)
    #     await self.bot.say(result)


def setup(bot):
    bot.add_cog(Dictionary(bot))
