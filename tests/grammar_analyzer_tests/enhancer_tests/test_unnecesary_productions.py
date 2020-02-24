from grammar_analyzer.enhancer.unnecesary_productions import (
    unreachable_remove,
    unitary_remove,
)
from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph
from pycmp.parsing import compute_firsts
from pycmp.utils import ContainerSet
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.grammar import Item


def test_unreachable_remove():
    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A
    S %= b

    A %= B

    B %= a

    C %= a

    new_grammar = unreachable_remove(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["A"], ["b"]]
    _graph["A"] = [["B"]]
    _graph["B"] = [["a"]]

    assert (new_grammar == _graph)


def test_unitary_remove():
    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A
    S %= b

    A %= B
    A %= a

    B %= a
    B %= C + b

    C %= a

    new_grammar = unitary_remove(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["a"], ["b"], ["C", "b"]]
    _graph["A"] = [["a"], ["C", "b"]]
    _graph["B"] = [["a"], ["C", "b"]]
    _graph["C"] = [["a"]]

    print(_graph)
    print(new_grammar)
    assert (new_grammar == _graph)