import asyncio

from async_lua import Environment, CommandExecutor

code = """
say("Sending message")
sleep(1)
say("...")
sleep(1)
say(message)
"""


class SayEnv(Environment):
    async def say(self, *args):
        """Prints a message"""
        print(*args)

    message = "Hello world!"


async def context():
    exec = CommandExecutor()
    exec.register_env(SayEnv)
    await exec.execute(code)


asyncio.run(context())
