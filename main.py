import asyncio

from embed.environment import Environment
from embed.executor import CommandExecutor

code = """
say("This is a message")
sleep(1)
say(item.name)
item.set('a', 5)
for i=1,10 do
    say(item.get('a'))
end
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
