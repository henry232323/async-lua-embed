import inspect


class DAO:
    """A class representing an interactable object similar to an environment, whose members can be accessed and
    whose async methods may be called from Lua seamlessly."""
    def __init__(self, dispatch):
        self._dispatch = dispatch
        for key, value in self.__class__.__dict__.items():
            if key.startswith("_"):
                continue
            if inspect.iscoroutinefunction(value):
                setattr(self, key, self._dispatch(value.__get__(self)))
