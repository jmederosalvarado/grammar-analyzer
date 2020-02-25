import json
from itertools import chain
from pycmp.grammar import Grammar, NonTerminal, Production, Sentence


def grammar_to_graph(grammar: Grammar):
    json_repr = json.loads(grammar.to_json)
    productions = {}
    for prod in json_repr["productions"]:
        bodies = productions.get(prod["head"], [])
        productions[prod["head"]] = [*bodies, prod["body"]]
    start_symbol = json_repr["start_symbol"]
    return start_symbol, productions


def graph_to_grammar(start_symbol: str, productions: dict):
    grammar = Grammar()
    for nt in productions.keys():
        is_start_symbol = nt == start_symbol
        grammar.add_nonterminal(nt, start_symbol=is_start_symbol)

    bodies = chain(*tuple(productions.values()))
    symbols = chain(*tuple(bodies))
    teminals = (s for s in symbols if grammar[s] is None)
    for t in teminals:
        grammar.add_terminal(t)

    for head, bodies in productions.items():
        for body in bodies:
            body = [grammar.epsilon] if body == "" else [grammar[s] for s in body]
            grammar.add_production(Production(grammar[head], Sentence(*body)))
    return grammar
