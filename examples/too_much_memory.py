import asyncio

from async_lua.executor import CommandExecutor

code = """
store = "000000000000000000000000000"
i = 0
while (true) do
    store = store .. store
end
"""


async def context():
    exec = CommandExecutor()
    await exec.execute(code)


asyncio.run(context())
