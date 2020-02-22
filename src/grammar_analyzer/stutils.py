from utils import visitor
from pycmp.utils import ContainerSet
from pycmp.grammar import NonTerminal, Terminal, EOF, Epsilon, Sentence


@visitor.on("obj")
def stformat(obj):
    return obj


@stformat.when(dict)
def stformat_dict(obj: dict):
    return {str(stformat(k)): stformat(v) for k, v in obj.items()}


@stformat.when(list)
def stformat_list(obj: list):
    return [stformat(i) for i in obj]


@stformat.when(tuple)
def stformat_tuple(obj: tuple):
    return tuple(stformat(i) for i in obj)


@stformat.when(set)
def stformat_set(obj: set):
    return tuple(stformat(i) for i in obj)


@stformat.when(ContainerSet)
def stformat_container_set(obj: ContainerSet):
    return {"symbols": stformat(obj.set), "epsilon": stformat(obj.contains_epsilon)}


@stformat.when(NonTerminal)
def stformat_nonterminal(obj: NonTerminal):
    return stformat(obj.name)


@stformat.when(Terminal)
def stformat_terminal(obj: Terminal):
    return stformat(obj.name)


@stformat.when(EOF)
def stformat_eof(obj: EOF):
    return "eof"


@stformat.when(Epsilon)
def stformat_epsilon(obj: Epsilon):
    return "epsilon"


@stformat.when(Sentence)
def stformat_sentence(obj: Sentence):
    return stformat(obj._symbols)

