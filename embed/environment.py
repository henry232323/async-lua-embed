import asyncio
import inspect
from functools import partial

from embed.models.item import Item


class Environment:
    def __init__(self, exec, dispatch):
        self.globals = exec.globals()

        for t in self.__class__.__mro__:
            for key, val in t.__dict__.items():
                if key.startswith("_"):
                    continue
                if inspect.iscoroutinefunction(val):
                    setattr(self.globals.sandbox.env, key, dispatch(val.__get__(self)))

        self.globals.sandbox.env.item = Item(dispatch, "Item name", {})

    async def sleep(self, time):
        await asyncio.sleep(time)
