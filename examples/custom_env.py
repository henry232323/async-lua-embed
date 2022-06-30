import asyncio

from src.async_lua import Environment, CommandExecutor

code = """
say("This is a message")
sleep(1)
say("This is another message")
"""


class SayEnv(Environment):
    async def say(self, *args):
        """Prints a message"""
        print(*args)


async def context():
    exec = CommandExecutor()
    exec.register_env(SayEnv)
    await exec.execute(code)


asyncio.run(context())
