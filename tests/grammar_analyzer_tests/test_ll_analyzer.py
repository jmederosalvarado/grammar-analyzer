from grammar_analyzer.ll_analyzer import build_conflict_str
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.utils import ContainerSet
from pycmp.parsing import build_ll_parser


def test_build_conflict_str():
    G = Grammar()

    S = G.add_nonterminal("S", True)
    A, B = G.add_nonterminals("A B")
    a, b = G.add_terminals("a b")

    S %= A + B
    A %= a + A | a
    B %= b + B | b

    table = {
        (S, a): [Production(S, Sentence(A, B))],
        (A, a): [Production(A, Sentence(a, A)), Production(A, Sentence(a))],
        (B, b): [Production(B, Sentence(b, B)), Production(B, Sentence(b))],
    }

    conflict_str = build_conflict_str(G)
    parser = build_ll_parser(G, table=table)

    try:
        parser(conflict_str)
        assert False
    except Exception:
        pass
