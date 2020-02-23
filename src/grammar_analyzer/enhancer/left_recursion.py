from pycmp.grammar import Grammar, Sentence, Symbol, Production, NonTerminal
from converter import grammar_to_graph, graph_to_grammar


def __direct_recursion_eliminate(d: dict):
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
    nonterminals = [t.name for t in G.nonterminals]

    S, d = grammar_to_graph(G)

    for i in range(0, len(nonterminals)):
        for j in range(0, i - 1):

            for sentence in d[nonterminals[i]]:
                if sentence[0] == nonterminals[j]:
                    d[i].remove(sentence)
                    new_sentence = sentence[1:len(sentence)]

                    for _sentence in d[nonterminals[j]]:
                        d[i].append(_sentence + [new_sentence])

        d = __direct_recursion_eliminate(d)

    return graph_to_grammar(S, d)


def epsilon_productions_eliminate(G):
    S, d = grammar_to_graph(G)
    nonterminals = [t.name for t in G.nonterminals]

    nullable = {}
    nullable = __find_nullable_nonterminals(d, nullable, S, nonterminals)

    for _, value in d.items():
        for sentence in value:

            if sentence[0] == "epsilon":
                value.remove(sentence)

            for i in range(0, len(sentence)):
                if sentence[i] in nonterminals and nullable[sentence[i]]:
                    new_sentence = sentence[0:i -
                                            1] + sentence[1 + 1:len(sentence)]

                    if not new_sentence in value:
                        value.append(new_sentence)

    if nullable[S]:
        d[S].append(["epsilon"])

    return graph_to_grammar(S, d)


def __find_nullable_nonterminals(d, nullable, symbol, nonterminals):

    try:
        _ = nullable[symbol]
        return nullable
    except KeyError:
        nullable[symbol] = False

    for Sentence in d[symbol]:
        local_nullable = True
        for symb in Sentence:
            if symb == "epsilon":
                break
            elif not symb in nonterminals:
                local_nullable = False
            else:
                nullable = __find_nullable_nonterminals(
                    d, nullable, symb, nonterminals)
                local_nullable = local_nullable and nullable[symb]

        nullable[symbol] = nullable[symbol] or local_nullable

    return nullable


def cycle_eliminate(G: Grammar):
    S, d = grammar_to_graph(G)
    nonterminals = [t.name for t in G.nonterminals]

    return graph_to_grammar(S, d)