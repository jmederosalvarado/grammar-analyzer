from itertools import chain
from pycmp.grammar import Grammar, NonTerminal, Production, Sentence

# TODO: Fix this, try to use grammar


def grammar_to_graph(grammar: Grammar):
    json_repr = grammar.to_json
    productions = {}
    for prod in json_repr["productions"]:
        bodies = productions.get(prod["head"], [])
        productions[prod["head"]] = [*bodies, prod["body"]]
    start_symbol = json_repr["start_symbol"]
    return start_symbol, productions


def graph_to_grammar(start_symbol: str, productions: dict):
    grammar = Grammar()
    for nt in productions.keys():
        grammar.add_nonterminal(nt, start_symbol=(nt == start_symbol))
    for t in chain(chain(productions.values)):
        if t not in grammar.nonterminals and t not in grammar.terminals:
            grammar.add_terminal(t)
    for head, bodies in productions:
        for body in bodies:
            if body == "":
                body = [grammar.epsilon]
            else:
                body = [grammar[s] for s in body]
            grammar.add_production(Production(head, Sentence(*body)))
    return grammar


def remove_left_recursion(grammar: Grammar):
    start_symbol, productions = grammar_to_graph(grammar)

    productions = remove_cycles(productions)
    productions = remove_epsilon_productions(productions)

    nonterminals = tuple(productions.keys())

    new_productions = {}
    for i, nti in enumerate(nonterminals):
        for ntj in nonterminals[:i]:
            for nti_body in productions[nti]:
                bodies: list = new_productions.get(nti, [])

                if nti_body[0] != ntj:
                    new_productions[nti] = [*bodies, nti_body]

                new_productions[nti] = bodies + [
                    ntj_body + nti_body[1:] for ntj_body in productions[ntj]
                ]

        new_productions = remove_inmediate_left_recursion(nti, new_productions[nti])

    return graph_to_grammar(start_symbol, productions)


def remove_inmediate_left_recursion(productions: dict, head: str):
    bodies = productions[head]
    left_rec = [body for body in bodies if body[0] == head]
    non_left_rec = [body for body in bodies if body[0] != head]

    if not left_rec:
        return productions

    head_prime = head + "_"
    return {
        **productions,
        **{
            head: [nlr + [head_prime] for nlr in non_left_rec],
            head_prime: [lr + [head_prime] for lr in left_rec] + [""],
        },
    }


def remove_cycles(productions: dict):
    return productions


def remove_epsilon_productions(productions: dict):
    return productions


def remove_common_prefixes(grammar: Grammar):
    start_symbol, productions = grammar_to_graph(grammar)
    nonterminals = productions.keys()
    for nt in nonterminals:
        productions = remove_common_prefixes_nonterminal(productions, nt)
    return graph_to_grammar(start_symbol, productions)


def remove_common_prefixes_nonterminal(productions: dict, nonterminal: str):

    return {}
