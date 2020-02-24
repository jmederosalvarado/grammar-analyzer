from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph
from pycmp.parsing import compute_firsts
from pycmp.utils import ContainerSet
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.grammar import Item

grammar = Grammar()
S = grammar.add_nonterminal("S", True)
A, B, C, X, Y = grammar.add_nonterminals("A B C X Y")
a, b, d, e = grammar.add_terminals("a b d e")

S %= A + B
S %= C

A %= C
A %= d

B %= Y

C %= a
C %= b
C %= X

X %= d
X %= e

Y %= e

_S, graph = grammar_to_graph(grammar)
new_grammar = graph_to_grammar(_S, graph)

_graph = {}
_graph["S"] = [["A", "B"], ["C"]]
_graph["A"] = [["C"], ["d"]]
_graph["B"] = [["Y"]]
_graph["C"] = [["a"], ["b"], ["X"]]
_graph["X"] = [["d"], ["e"]]
_graph["Y"] = [["e"]]

assert (graph == _graph)
