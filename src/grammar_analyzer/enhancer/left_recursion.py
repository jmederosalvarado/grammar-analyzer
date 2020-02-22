from pycmp.grammar import Grammar, Sentence, Symbol, Production, NonTerminal
from converter import grammar_to_graph, graph_to_grammar


def direct_recursion_eliminate(d: dict):
    new_productions = []

    for key, value in d.items():
        recursion = []
        no_recursion = []
        for sentence in value:
            if sentence._symbols[0] == key:
                recursion.append(sentence)
            else:
                no_recursion.append(sentence)

        if len(recursion) == 0:
            for sentence in no_recursion:
                new_productions.append((key, sentence))

        # there's some left recursion
        else:
            X = (key.name + "'")

            for sentence in no_recursion:
                sentence.append(X)
                new_productions.append((key, sentence))

            for sentence in recursion:
                new_sentence = []
                for symb in sentence:
                    if symb == key:
                        continue
                    new_sentence.append(symb)
                new_sentence.append(X)
                new_productions.append((X, new_sentence))

            new_productions.append((X, ["epsilon"]))

    new_d = {}

    for p in new_productions:
        try:
            new_d[p.left].append(p.right)
        except:
            new_d[p.left] = [p.right]

    return new_d


def general_recursion_eliminate(G):
    new_productions = []

    for p in G.productions:
        new_productions.append(p)

    terminals = [t.name for t in G.terminals]

    S, d = grammar_to_graph(G)

    for i in range(0, len(terminals)):
        for j in range(0, i - 1):

            for sentence in d[terminals[i]]:
                if sentence[0] == terminals[j]:
                    d[i].remove(sentence)
                    new_sentence = sentence[1:len(sentence)]

                    for _sentence in d[terminals[j]]:
                        d[i].append(_sentence + [new_sentence])

        for key, value in d.items():
            new_productions.append((key, value))

        d = direct_recursion_eliminate(d)

    return graph_to_grammar(S, d)
