from inspect import signature

registry = {}  # type: dict


class Visitor(object):
    def __init__(self, params, default=None):
        self.params = params
        self.typemap = {}
        self.default = default

    def __call__(self, *args):
        types = tuple(args[i].__class__ for i in self.params)
        function = self.typemap.get(types, self.default)
        return function(*args)

    def register(self, types, function):
        assert types not in self.typemap, "Already registered types"
        self.typemap[types] = function

    def when(self, *types):
        assert len(types) == len(
            self.params
        ), "The amout of types must match the amount of parameters"

        def register(function):
            self.register(types, function)
            return function

        return register


def on(*argnames):
    def register(function):
        name = function.__name__
        params = signature(function).parameters
        params = [i for i, p in enumerate(params) if p in argnames]

        registry[name] = Visitor(params, default=function)

        return registry[name]

    return register
