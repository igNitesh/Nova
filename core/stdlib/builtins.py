class BuiltInFunction:
    def __init__(self, func):
        self.func = func

    def call(self, args):
        return self.func(args)