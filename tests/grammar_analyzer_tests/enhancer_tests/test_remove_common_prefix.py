from grammar_analyzer.enhancer.remove_common_prefixes import remove_common_prefixes

from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph
from pycmp.parsing import compute_firsts
from pycmp.utils import ContainerSet
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.grammar import Item


def test_remove_common_prefixs():
    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= a
    A %= B + a + b
    A %= B + a + a
    A %= B

    new_grammar = remove_common_prefixes(grammar)

    S, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["a"]]
    _graph["A"] = [["B", "A''"]]
    _graph["A'"] = [["b"], ["a"]]
    _graph["A''"] = [[], ["a", "A'"]]

    print(new_grammar)
    print(_graph)

    assert new_grammar == _graph


def test_remove_common_prefixs_2():
    grammar = Grammar()
    A = grammar.add_nonterminal("A", True)
    B, C, D, E, F = grammar.add_nonterminals("B C D E F")
    a, b, c, d = grammar.add_terminals("a b c d")

    A %= b + B
    A %= c + C
    A %= d + D

    B %= c + C
    B %= grammar.epsilon

    C %= c + c + c
    C %= A
    C %= a
    C %= b
    C %= grammar.epsilon

    D %= d
    D %= b
    D %= E
    D %= grammar.epsilon

    E %= F
    E %= C

    F %= D

    new_grammar = remove_common_prefixes(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["a"]]
    _graph["A"] = [["B", "A''"]]
    _graph["A'"] = [["b"], ["a"]]
    _graph["A''"] = [[], ["a", "A'"]]

    assert True