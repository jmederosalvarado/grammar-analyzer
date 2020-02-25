from pycmp.grammar import Grammar, Sentence, Symbol, Production, NonTerminal
from grammar_analyzer.enhancer.converter import grammar_to_graph, graph_to_grammar
from grammar_analyzer.enhancer.unnecesary_productions import (
    unitary_remove,
    unreachable_remove,
)


def remove_left_recursion(grammar):
    new_grammar = __remove_epsilon_productions(grammar)
    new_grammar = unitary_remove(new_grammar)
    new_grammar = unreachable_remove(new_grammar)

    nonterminals = [t.name for t in new_grammar.nonterminals]

    S, d = grammar_to_graph(new_grammar)

    for i in range(0, len(nonterminals)):
        for j in range(0, i):
            for sentence in d[nonterminals[i]]:
                if sentence[0] == nonterminals[j]:
                    d[nonterminals[i]].remove(sentence)
                    remove_first = sentence[1 : len(sentence)]

                    for sentence in d[nonterminals[j]]:
                        new_sentence = []
                        for item in sentence:
                            new_sentence.append(item)
                        for item in remove_first:
                            new_sentence.append(item)
                        d[nonterminals[i]].append(new_sentence)
        d = __remove_inmediate_left_recursion(d)

    return graph_to_grammar(S, d)


def __remove_inmediate_left_recursion(d: dict):
    new_productions = []

    for key, value in d.items():
        recursion = []
        no_recursion = []
        for sentence in value:
            if sentence == []:
                no_recursion.append(sentence)
            elif sentence[0] == key:
                recursion.append(sentence)
            else:
                no_recursion.append(sentence)

        if len(recursion) == 0:
            for sentence in no_recursion:
                new_productions.append((key, sentence))

        # there's some left recursion
        else:
            X = key + "'"

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

            new_productions.append((X, []))

    new_d = {}

    for p in new_productions:
        try:
            new_d[p[0]].append(p[1])
        except:
            new_d[p[0]] = [p[1]]

    return new_d


def __remove_epsilon_productions(grammar):
    S, d = grammar_to_graph(grammar)
    nonterminals = [t.name for t in grammar.nonterminals]

    nullable = {}
    nullable = __find_nullable_nonterminals(d, nullable, S, nonterminals)

    for key, value in d.items():
        new_value = [v for v in value]

        for sentence in value:
            if sentence == []:
                new_value.remove(sentence)

            for i in range(0, len(sentence)):
                if sentence[i] in nonterminals and nullable[sentence[i]]:
                    new_sentence = sentence[0:i] + sentence[i + 1 : len(sentence)]

                    if not new_sentence in new_value:
                        new_value.append(new_sentence)

        d[key] = new_value

    if nullable[S]:
        d[S].append([])

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
                nullable = __find_nullable_nonterminals(d, nullable, symb, nonterminals)
                local_nullable = local_nullable and nullable[symb]

        nullable[symbol] = nullable[symbol] or local_nullable

    return nullable
