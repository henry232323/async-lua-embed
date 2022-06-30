"""
Sandboxing:
- https://stackoverflow.com/questions/1224708/how-can-i-create-a-secure-lua-sandbox
- https://github.com/scrapinghub/splash/blob/master/splash/lua_modules/sandbox.lua
- https://github.com/scoder/lupa/issues/47


Model:
- A separate thread (a subprocess should work) is provisioned for executing the lua
  - The thread has a time limit on execution, and will be killed
    - Its hard to kill threads, easy to kill subprocesses, IPC is difficult however
  - The thread uses a queue to request async executions from the bot, and receives the responses back
  - https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call

- DAOs are used to allow scripters to update objects like items' and characters' attributes from scripts
- Asynchronous nature is maintained by suspending execution with coroutines until async completes
  - Commands are yielded by the coroutine, processed, and sent back into the coro
"""

from .executor import CommandExecutor