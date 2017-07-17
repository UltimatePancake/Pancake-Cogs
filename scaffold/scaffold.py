from __future__ import unicode_literals

import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems

import falcon

import asyncio
import discord
import functools
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands


NUM_THREADS = 4
BINDING = ['localhost', '8080']


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def handler_app(environ, start_response):
    response_body = b'Works fine'
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return [response_body]


class Bird(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(Bird, self).__init__()

    def load_config(self):
        config = dict([
            (key, value) for key, value in iteritems(self.options) if key in self.cfg.settings and value is not None
        ])

        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    class ThingsResource(object):
        def on_get(self, req, resp):
            """Handles GET requests"""
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = ('\nTwo things awe me most, the starry sky '
                         'above me and the moral law within me.\n'
                         '\n'
                         '    ~ Immanuel Kant\n\n')

    # falcon.API instances are callable WSGI apps
    app = falcon.API()

    # Resources are represented by long-lived class instances
    things = ThingsResource()

    # things will handle all requests to the '/things' URL path
    app.add_route('/things', things)



class Scaffold:
    """Kowlin's worst nightmare"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @asyncio.coroutine
    def start_coro(self):
        print("coro")
        options = {
            'bind': '{}:{}'.format(BINDING[0], BINDING[1]),
            'workers': number_of_workers(),
            'worker_class': 'gevent',
        }
        print("options set")
        yield from asyncio.sleep(1)
        print("slept")
        Bird(handler_app, options).run()
        print("run bird")
        asyncio.async(self.start_coro)

    @commands.command(name="start")
    async def start(self):
        """DUUUUUUUURP"""
        print("a'fore shit goes down")
        task = functools.partial(self.start_coro)
        print(task)
        task = self.bot.loop.run_in_executor(None, task)
        print(task)
        up = await asyncio.wait_for(task, timeout=30)
        print(up)
        if up:
            await self.bot.say("started")


def setup(bot):
    bot.add_cog(Scaffold(bot))
