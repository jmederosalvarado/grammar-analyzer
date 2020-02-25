from grammar_analyzer.enhancer.remove_common_prefixes import remove_common_prefixes

from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph
from pycmp.parsing import compute_firsts
from pycmp.utils import ContainerSet
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.grammar import Item


def test_remove_unreachable_prods():
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
