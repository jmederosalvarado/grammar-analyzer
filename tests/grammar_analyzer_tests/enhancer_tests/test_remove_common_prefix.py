# from grammar_analyzer.enhancer.remove_common_prefix import remove_common_prefixes
# from pycmp.parsing import compute_firsts
# from pycmp.utils import ContainerSet
# from pycmp.grammar import Grammar, Sentence, Production
# from pycmp.grammar import Item

# grammar = Grammar()
# S = grammar.add_nonterminal("S", True)
# A, B, C, X, Y = grammar.add_nonterminals("A B C X Y")
# a, b, d, e = grammar.add_terminals("a, b, d, e")

# S %= A + B
# S %= C

# A %= C
# A %= d

# B %= Y

# C %= a
# C %= b
# C %= X

# X %= d
# X %= e

# Y %= e