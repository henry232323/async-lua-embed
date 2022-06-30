import asyncio
import inspect


class Environment:
    def __init__(self, exec, dispatch):
        self.globals = exec.globals()
        self._exec = exec
        self._dispatch = dispatch

        for t in self.__class__.__mro__:
            for key, val in t.__dict__.items():
                if key.startswith("_"):
                    continue
                if inspect.iscoroutinefunction(val):
                    setattr(self.globals.sandbox.env, key, dispatch(val.__get__(self)))

    def register(self, key, value):
        self.globals.sandbox.env[key] = value

    async def sleep(self, time):
        await asyncio.sleep(time)
