import asyncio
import inspect

from lupa import LuaRuntime


class Environment:
    """Defines a class for which members (including async functions) can be accessed and run from within Lua"""

    def __init__(self, runtime: LuaRuntime, dispatch: callable):
        self.globals = runtime.globals()
        self._runtime = runtime
        self._dispatch = dispatch

        for cls in self.__class__.__mro__:
            for key, value in cls.__dict__.items():
                if key.startswith("_"):
                    continue
                self.register(key, value)

    def register(self, key, value):
        """Register a global variable with the Lua script, may accept a static value or a function / async function"""
        if inspect.iscoroutinefunction(value):
            self.globals.sandbox.env[key] = self._dispatch(value.__get__(self))
        else:
            self.globals.sandbox.env[key] = value

    async def sleep(self, time):
        """Suspend execution for a set duration < 3600s"""
        if time > 3600:
            raise RuntimeError("Can't sleep more than an hour")
        await asyncio.sleep(time)
