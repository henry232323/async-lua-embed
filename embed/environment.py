from functools import partial

from embed.models.item import Item

set_env_code = """{
  ipairs = ipairs,
  next = next,
  pairs = pairs,
  tonumber = tonumber,
  tostring = tostring,
  type = type,
  unpack = unpack,
  coroutine = { create = coroutine.create, resume = coroutine.resume, 
      running = coroutine.running, status = coroutine.status, 
      wrap = coroutine.wrap, yield = coroutine.yield },
  string = { byte = string.byte, char = string.char, find = string.find, 
      format = string.format, gmatch = string.gmatch, gsub = string.gsub, 
      len = string.len, lower = string.lower, match = string.match, 
      rep = string.rep, reverse = string.reverse, sub = string.sub, 
      upper = string.upper },
  table = { insert = table.insert, maxn = table.maxn, remove = table.remove, 
      sort = table.sort },
  math = { abs = math.abs, acos = math.acos, asin = math.asin, 
      atan = math.atan, atan2 = math.atan2, ceil = math.ceil, cos = math.cos, 
      cosh = math.cosh, deg = math.deg, exp = math.exp, floor = math.floor, 
      fmod = math.fmod, frexp = math.frexp, huge = math.huge, 
      ldexp = math.ldexp, log = math.log, log10 = math.log10, max = math.max, 
      min = math.min, modf = math.modf, pi = math.pi, pow = math.pow, 
      rad = math.rad, random = math.random, sin = math.sin, sinh = math.sinh, 
      sqrt = math.sqrt, tan = math.tan, tanh = math.tanh },
  os = { clock = os.clock, difftime = os.difftime, time = os.time },
}"""


class Environment:
    def __init__(self, ctx, exec, dispatch):
        self.ctx = ctx

        env = exec.eval(set_env_code)
        self.globals = exec.globals()
        for item in self.globals:
            del self.globals[item]

        for key, val in env.items():
            self.globals[key] = val

        for key, val in type(self).__dict__.items():
            if key.startswith("_"): continue
            if callable(val):
                setattr(self.globals, key, dispatch(self.say))

        self.globals['item'] = Item(dispatch, "Item name", {})

    async def get_command(self):
        pass

    async def say(self, message):  # async
        print(message)