import asyncio
import concurrent.futures
import pathlib
from typing import Type, List

from lupa import LuaRuntime

from .environment import Environment


def filter_attribute_access(obj, attr_name, is_setting):
    if isinstance(attr_name, str):
        if not attr_name.startswith('_'):
            return attr_name
    raise AttributeError()


"""
Information on Sandboxing
https://github.com/scrapinghub/splash/blob/master/splash/lua_modules/sandbox.lua
https://github.com/scoder/lupa/issues/47
"""
with open(pathlib.Path(__file__).parents[0] / "sandbox.lua") as sbfile:
    sandbox = sbfile.read()


class CommandExecutor:
    """A class used to execute Lua code snippits"""

    def __init__(self):
        self._runtime = LuaRuntime(unpack_returned_tuples=True,
                                   register_builtins=False,
                                   register_eval=False,
                                   attribute_filter=filter_attribute_access)
        self.environments: List[Environment] = []

        self._event_loop = asyncio.get_running_loop()
        if self._event_loop is None:
            raise RuntimeError("CommandExecutor must be instantiated in an async context")

        self._sandbox = self._runtime.execute(sandbox)
        self._runtime.globals().sandbox = self._sandbox

        # A Lua function wrapper that allows Python functions to be yielded from Lua coroutines
        # to be run by `_execute`
        self._dispatch = self._runtime.eval("""
            function (func)
                function inner(...)
                    return coroutine.yield(func, ...)
                end
                return inner
            end
        """)

        self.environments.append(Environment(self._runtime, self._dispatch))

    def register_env(self, env: Type[Environment]):
        """Register a new set of functions that will be accessible at the top level"""
        self.environments.append(env(self._runtime, self._dispatch))

    async def execute(self, code: str):
        """Asynchronously execute a Lua code excerpt in a separate thread"""
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await self._event_loop.run_in_executor(
                pool, self._execute, code
            )

    def _execute(self, code: str):
        """Evaluate the Lua code and execute the coroutine step by step"""
        coro = self._sandbox.create_coroutine(self._sandbox.run(code)).coroutine()
        last = None

        while True:
            try:
                result = coro.send(last)
                # Lua coroutine.yield will yield a single item rather than a singleton tuple
                if not isinstance(result, tuple):
                    result = (result,)

                command, *args = result
                command_coro = command(*args)
                future = asyncio.run_coroutine_threadsafe(command_coro, self._event_loop)
                last = future.result()
            except StopIteration as e:
                return e.value