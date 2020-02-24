from pycmp.grammar import Grammar
from grammar_analyzer.slr_analyzer import is_slr_grammar


def test_is_slr_grammar():
    GG = Grammar()

    S = GG.add_nonterminal("S", True)
    X = GG.add_nonterminal("X")
    if_, then, else_, num = GG.add_terminals("if then else num")

    S %= if_ + X + then + S
    S %= if_ + X + then + S + else_ + S
    S %= num
    X %= num

    assert is_slr_grammar(GG) == False
