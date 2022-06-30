# Async Lua Embed
This small package is intended to provide the tools to allow the embedding of user generated scripts into 
an async environment. This package allows the definition and execution of asynchronous Python functions
and methods in the user defined scripts, which may allow users to interface with things like Discord bot

### Installation

```shell
python -m pip install git+https://github.com/henry232323/async-lua-embed
```

### Example
For an example of most of the package's functionality:

```python
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
  def __init__(self, exec, dispatch):
    super().__init__(exec, dispatch)

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

```

### Sandboxing
This library implements a simple sandbox based on some of the links below, including the final
module wholesale.
- https://stackoverflow.com/questions/1224708/how-can-i-create-a-secure-lua-sandbox
- https://github.com/scoder/lupa/issues/47
- https://github.com/scrapinghub/splash/blob/master/splash/lua_modules/sandbox.lua

### Model
- Open an executor in which the Lua will be executed
- Run all Lua in an elaborate sandbox limiting access, memory, and number of instructions
- No need to kill threads when the sandbox (hopefully) manages itself
- A DAO is intended to be a surrogate for seamlessly embedding async functions into an object, allowing control
over the object with Python implemented async functions
- Asynchronous nature is maintained by suspending execution with coroutines until async completes
  - Commands are yielded by the coroutine, processed, and sent back into the coro
