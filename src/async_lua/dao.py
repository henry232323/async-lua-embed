import inspect


class DAO:
    def __init__(self, dispatch):
        self.dispatch = dispatch
        for key, value in self.__class__.__dict__.items():
            if key.startswith("_"): continue
            if inspect.iscoroutinefunction(value):
                setattr(self, key, self.dispatch(value.__get__(self)))
