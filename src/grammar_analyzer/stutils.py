from utils import visitor


@visitor.on("obj")
def stformat(obj):
    return obj


@stformat.when(dict)
def stformat_dict(obj):
    return {stformat(k): stformat(v) for k, v in obj.items()}


@stformat.when(list)
def stformat_list(obj):
    return [stformat(i) for i in obj]


@stformat.when(tuple)
def stformat_tuple(obj):
    return tuple(stformat(i) for i in obj)


@stformat.when(set)
def stformat_set(obj):
    return set(stformat(i) for i in obj)
