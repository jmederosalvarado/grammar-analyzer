from pycmp.grammar import Grammar, Sentence, Symbol, Production, NonTerminal
from converter import grammar_to_graph, graph_to_grammar


def unreachable_eliminate(G: Grammar):
    S, d = grammar_to_graph(G)
    terminals = [t.name for t in G.terminals]

    mark = {}

    for p in d.keys():
        mark[p.left] = False

    overlook(d, mark, terminals, G.start_symbol)

    for t in terminals:
        if not mark[t]:
            _ = d.pop(t)

    return graph_to_grammar(S, d)


def overlook(d: dict, mark: dict, terminals: list, t):
    mark[t] = True
    for sentence in d[t]:
        if len(sentence._symbols) == 1 and not sentence._symbols[
                0].is_epsilon and sentence._symbols[0].is_nonterminal:
            overlook(d, mark, terminals, sentence._symbols[0])


def useless_eliminate(G: Grammar):
    S, d = grammar_to_graph(G)

    for _, value in d.items():
        for sentence in value:
            if len(sentence) == 1 and not sentence._symbols[
                    0].is_epsilon and sentence._symbols[0].is_nonterminal:
                value.remove(sentence)
                for item in d[sentence[0]]:
                    value.append(item)

    return graph_to_grammar(S, d)