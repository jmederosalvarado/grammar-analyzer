from inspect import signature

registry = {}


class Visitor(object):
    def __init__(self, params):
        self.params = params
        self.typemap = {}

    def __call__(self, *args):
        types = tuple(args[i].__class__ for i in self.params)
        function = self.typemap[types]
        return function(*args)

    def register(self, types, function):
        assert types not in self.typemap
        self.typemap[types] = function

    def when(self, *types):
        assert len(types) == len(self.params)

        def register(function):
            self.register(types, function)
            return function

        return register


def on(*argnames):
    def register(function):
        name = function.__name__
        params = signature(function).parameters
        params = [i for i, p in enumerate(params) if p in argnames]

        assert name not in registry
        registry[name] = Visitor(params)

        return registry[name]

    return register
