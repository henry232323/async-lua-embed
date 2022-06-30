import asyncio

from src.async_lua.executor import CommandExecutor

code = """
while (true) do
    a = 5
end
"""


async def context():
    exec = CommandExecutor()
    await exec.execute(code)


asyncio.run(context())
