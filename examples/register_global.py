import asyncio

from async_lua import Environment, CommandExecutor

code = """
say("Hello!")
sleep(1)
say("My name is...")
sleep(1)
say(username .. "!")
"""


class SayEnv(Environment):
    def __init__(self, exec, dispatch):
        super().__init__(exec, dispatch)

        self.register("username", "henry232323")

    async def say(self, *args):
        """Prints a message"""
        print(*args)


async def context():
    exec = CommandExecutor()
    exec.register_env(SayEnv)
    await exec.execute(code)


asyncio.run(context())
