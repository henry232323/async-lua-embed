import asyncio

from embed.executor import CommandExecutor

code = """
function ()
    say(item.name)
    item.set('a', 5)
    for i=1,10 do
        say(item.get('a'))
    end
end
"""

exec = CommandExecutor(code)
asyncio.run(exec.proc())
