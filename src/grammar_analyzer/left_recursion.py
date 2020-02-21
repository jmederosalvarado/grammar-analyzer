from pycmp.grammar import Grammar, Sentence, Symbol, Production, NonTerminal


def direct_recursion_eliminate(G: Grammar):
    new_G = G
    productions = new_G.productions
    new_productions = []

    d = {}

    for p in productions:
        try:
            d[p.left].append(p.right)
        except:
            d[p.left] = [p.right]

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
                new_productions.append(Production(key, sentence))

        # there's some left recursion
        else:
            X = NonTerminal(key.name + "'", new_G)

            for sentence in no_recursion:
                new_productions.append(Production(key, Sentence(sentence, X)))

            for sentence in recursion:
                new_sentence = []
                for symb in sentence:
                    if symb == key:
                        continue
                    new_sentence.append(symb)
                new_productions.append(
                    Production(X, Sentence(*new_sentence, X)))
            new_productions.append(Production(X, new_G.epsilon))

    new_G.productions = new_productions
    return new_G


def general_recursion_eliminate(G):
    new_G = G
    productions = new_G.productions
    new_productions = []
    for p in productions:
        new_productions.append(p)

    terminals = new_G.terminals

    d = {}
    for p in new_productions:
        try:
            d[p.left].append(p.right)
        except:
            d[p.left] = [p.right]

    for i in range(0, len(terminals)):
        for j in range(0, i - 1):

            for sentence in d[terminals[i]]:
                if sentence._symbols[0] == terminals[j]:
                    d[i].remove(sentence)
                    new_sentence = sentence._symbols[1:len(sentence._symbols)]

                    for _sentence in d[terminals[j]]:
                        d[i].append(
                            Sentence(*_sentence._symbols, *new_sentence))

        for key, value in d.items():
            new_productions.append(Production(key, value))

        new_G.productions = new_productions
        new_G = direct_recursion_eliminate(new_G)

        new_productions = []

        return new_G
