from grammar_analyzer.regular_analyzer import (is_regular_grammar,
                                               grammar_to_automaton,
                                               automaton_to_regex,
                                               __automaton_to_gnfa)
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.utils import ContainerSet
from pycmp.parsing import build_ll_parser
from pycmp.regex import Regex
from pycmp.automata import DFA
from pycmp.utils import pprint


def test_is_regular():
    G = Grammar()

    S = G.add_nonterminal("S", True)
    A, B = G.add_nonterminals("A B")
    a, b = G.add_terminals("a b")

    S %= a + A
    S %= b + B
    A %= a + A
    A %= a
    B %= b + B
    B %= b

    assert is_regular_grammar(G)


def test_gramar_to_automaton():
    pass
    G = Grammar()

    S = G.add_nonterminal("S", True)
    A, B = G.add_nonterminals("A B")
    a, b = G.add_terminals("a b")

    S %= a + A
    S %= b + B
    A %= a + A
    A %= a
    B %= b + B
    B %= b

    aut = grammar_to_automaton(G)


def test_automaton_to_regex():
    G = Grammar()

    S = G.add_nonterminal("S", True)
    a, b = G.add_terminals("a b")

    S %= a + S
    S %= a
    S %= b

    aut = grammar_to_automaton(G)

    aut.graph().write("/home/rodrigo/Projects/grammar_analizer/graph",
                      format="svg")

    regex = automaton_to_regex(aut)

    print(regex)

    r = Regex(regex)

    assert r("aaaaaaaaaab")
    assert not r("aaaaaaaaaabbbbbb")
    assert not r("bababbbbabb")

    # transitions = {(0, "a"): 0, (0, "b"): 1, (1, "a"): 1, (1, "b"): 1}

    # autom = DFA(2, {1}, transitions)
    # gnfa = __automaton_to_gnfa(autom)

    # pprint(gnfa[1])
    # assert False
