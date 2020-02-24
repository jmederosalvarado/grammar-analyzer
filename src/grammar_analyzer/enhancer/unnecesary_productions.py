from pycmp.grammar import Grammar, Sentence, Symbol, Production, NonTerminal
from grammar_analyzer.enhancer.converter import grammar_to_graph, graph_to_grammar


def unreachable_remove(G: Grammar):
    S, d = grammar_to_graph(G)
    nonterminals = [t.name for t in G.nonterminals]

    mark = {}

    for p in d.keys():
        mark[p.left] = False

    __overlook(d, mark, nonterminals, G.start_symbol)

    for t in nonterminals:
        if not mark[t]:
            _ = d.pop(t)

    return graph_to_grammar(S, d)


def __overlook(d: dict, mark: dict, nonterminals: list, t):
    mark[t] = True
    for sentence in d[t]:
        if len(sentence) == 1 and sentence[0] in nonterminals:
            __overlook(d, mark, nonterminals, sentence[0])


def unitary_remove(G: Grammar):
    S, d = grammar_to_graph(G)
    nonterminals = [t.name for t in G.nonterminals]
    new_d = []

    u = __find_unitary_pairs(d, nonterminals)

    for pair in u:
        for sentence in d[pair[1]]:
            if not (len(sentence) == 1 and sentence[0] in nonterminals):
                try:
                    new_d[pair[0]].append(sentence)
                except KeyError:
                    new_d[pair[0]] = [sentence]

    return graph_to_grammar(S, new_d)


def __find_unitary_pairs(d, nonterminals):

    pairs = [()]
    for key, value in d.items():
        for sentence in value:
            if len(sentence) == 1 and sentence[0] in nonterminals:
                pairs.append(key, sentence[0])

    for nt in nonterminals:
        reachable = []
        reachable = __look_forward(pairs, nt, reachable)

        pairs.append(nt, nt)
        for r in reachable:
            if not (nt, r) in pairs:
                pairs.append((nt, r))

    return pairs


def __look_forward(pairs, nt, _list):

    for pair in pairs:
        if pair[0] == nt:
            if not pair[1] in _list:
                _list.append(pair[1])
                _list = __look_forward(pairs, pair[1], _list)

    return _list
