import pydot
from functools import lru_cache
from pycmp.grammar import Grammar
from pycmp.parsing import build_ll_table as __build_ll_table
from pycmp.parsing import build_ll_parser
from grammar_analyzer.basic_analyzer import compute_firsts, compute_follows


@lru_cache
def is_ll_grammar(grammar):
    table = build_ll_table(grammar)
    return not any(len(v) > 1 for v in table.values())


@lru_cache
def build_ll_table(grammar):
    firsts = compute_firsts(grammar)
    follows = compute_follows(grammar)
    return __build_ll_table(grammar, firsts, follows)


@lru_cache
def build_conflict_str(grammar):
    table = build_ll_table(grammar)
    start, terminals = grammar.start_symbol, grammar.terminals
    return __build_conflict_str([start], table, terminals, set())


def __build_conflict_str(stack, table, terminals, visited):
    if len(stack) == 0:
        return None

    top = stack.pop()

    if top.is_terminal:
        conflict = __build_conflict_str(stack, table, terminals, visited)
        if conflict is None:
            return None
        return [top] + conflict

    for t in terminals:
        if (top, t) in visited:
            continue
        try:
            production = table[top, t]
        except KeyError:
            continue
        if len(production) > 1:
            return [t]
        production = production[0]
        visited.add((top, t))
        conflict = __build_conflict_str(
            stack + list(reversed(production.right)), table, terminals, visited
        )
        if conflict is None:
            continue
        return conflict

    return None


def get_derivation_tree_builder(grammar):
    table = build_ll_table(grammar)
    parser = build_ll_parser(grammar, table=table)

    @lru_cache
    def tree_builder(tokens):
        left_parse = parser(tokens)
        tree = pydot.Graph(graph_type="graph")
        __build_tree(iter(left_parse), tree)
        return tree

    return tree_builder


def __build_tree(left_parse, tree):
    production = next(left_parse)
    node = production.left.name
    for s in production.right:
        if not s.is_terminal and not s.is_epsilon:
            __build_tree(left_parse, tree)
        edge = pydot.Edge(node, s.name)
        tree.add_edge(edge)
