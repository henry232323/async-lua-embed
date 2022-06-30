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
    def __init__(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True,
                              register_eval=False,
                              attribute_filter=filter_attribute_access)
        self.envs: List[Environment] = []

        self.event_loop = asyncio.get_running_loop()
        if self.event_loop is None:
            raise RuntimeError("CommandExecutor must be instantiated in an async context")

        self.sandbox = self.lua.execute(sandbox)
        self.lua.globals()['sandbox'] = self.sandbox
        self.dispatch = self.lua.eval("""
            function (func)
                function inner(...)
                    return coroutine.yield(func, ...)
                end
                return inner
            end
        """)

        self.envs.append(Environment(self.lua, self.dispatch))

    def register_env(self, env: Type[Environment]):
        self.envs.append(env(self.lua, self.dispatch))

    async def execute(self, code):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await self.event_loop.run_in_executor(
                pool, self._execute, code
            )

    def _execute(self, code):
        coro = self.sandbox.create_coroutine(self.sandbox.run(code)).coroutine()
        last = None

        while True:
            try:
                res = coro.send(last)
                if not isinstance(res, tuple):
                    res = (res,)

                command, *args = res
                command_coro = command(*args)
                future = asyncio.run_coroutine_threadsafe(command_coro, self.event_loop)
                last = future.result()
            except StopIteration:
                break
