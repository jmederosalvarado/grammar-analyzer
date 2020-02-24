from itertools import chain
from pycmp.grammar import Grammar, NonTerminal, Production, Sentence
import json


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
        grammar.add_nonterminal(nt, start_symbol=(nt == start_symbol))

    for _, value in productions.items():  # TODO: Refactor
        for string in value:
            for t in string:
                if grammar[t] is None:
                    grammar.add_terminal(t)

    for head, bodies in productions.items():
        for body in bodies:
            if body == "":
                body = [grammar.epsilon]
            else:
                body = [grammar[s] for s in body]

            grammar.add_production(Production(grammar[head], Sentence(*body)))
    return grammar