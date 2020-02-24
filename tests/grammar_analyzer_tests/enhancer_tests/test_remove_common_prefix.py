# from pycmp.grammar import Grammar
# from grammar_analyzer.enhancer.unnecesary_productions import unitary_remove, unreachable_remove
# from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph

# ################################################################################################################
# # epsilon test #1
# grammar = Grammar()
# S = grammar.add_nonterminal("S", True)
# A, B, C = grammar.add_nonterminals("A B C")
# a, b = grammar.add_terminals("a b")

# S %= A + B
# S %= C

# A %= b + A + b
# A %= grammar.epsilon

# B %= b

# C %= a
# C %= b

# new_grammar = epsilon_productions_remove(grammar)

# _, new_grammar = grammar_to_graph(new_grammar)

# _graph = {}
# _graph["S"] = [["A", "B"], ["C"], ["B"]]
# _graph["A"] = [["b", "A", "b"], ["b", "b"]]
# _graph["B"] = [["b"]]
# _graph["C"] = [["a"], ["b"]]

# assert (new_grammar == _graph)
