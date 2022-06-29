from lupa import LuaRuntime

from embed.environment import Environment


def filter_attribute_access(obj, attr_name, is_setting):
    if isinstance(attr_name, str):
        if not attr_name.startswith('_'):
            return attr_name
    raise AttributeError()


class CommandExecutor:
    def __init__(self, code):
        self.lua = LuaRuntime(unpack_returned_tuples=True,
                              register_eval=False,
                              attribute_filter=filter_attribute_access)
        self.code = code
        self.dispatch = self.lua.eval("""
        function (func)
            function inner(...)
                coroutine.yield(func, ...)
            end
            return inner
        end
        """)
        self.env = Environment(5, self.lua, self.dispatch)

    async def proc(self):  # async
        coro = self.lua.eval(self.code).coroutine()  # aka thread
        last = None
        while True:
            try:
                command, *args = coro.send(last)
                last = await command(*args)
            except StopIteration:
                break
