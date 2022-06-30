import asyncio

import aiohttp as aiohttp

from async_lua import DAO, Environment, CommandExecutor


class Pokemon(DAO):
    def __init__(self, dispatch, name):
        super().__init__(dispatch)
        self.name: str = name

    async def get_type(self):
        async with aiohttp.ClientSession() as session:
            data = await session.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
            js = await data.json()
            return js["types"][0]["type"]["name"]


class ApiEnvironment(Environment):
    def __init__(self, runtime, dispatch):
        super().__init__(runtime, dispatch)

        self.register("ditto", Pokemon(dispatch, "ditto"))

    async def say(self, *args):
        """Prints a message"""
        print(*args)


code = """
say(ditto.get_type())
"""


async def context():
    exec = CommandExecutor()
    exec.register_env(ApiEnvironment)
    await exec.execute(code)


asyncio.get_event_loop().run_until_complete(context())
