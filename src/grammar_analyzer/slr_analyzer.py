from functools import lru_cache
from pycmp.parsing import SLR1Parser, build_lr0_automaton
from grammar_analyzer.shift_reduce_analyzer import (
    shift_reduce_info,
    build_conflict_str as __build_conflict_str,
)
from grammar_analyzer.common import build_derivation_tree

# TODO: Refactor all shift-reduce analyzers to share common code


class __SLR1ParserConflicts(SLR1Parser):
    def __call__(self, tokens, return_actions=False):
        raise NotImplementedError()

    @staticmethod
    def _register(table, key, value):
        if key in table and value not in table[key]:
            table[key].append(value)
        else:
            table[key] = [value]


@lru_cache
def __build_slr_info(grammar):
    parser_conflicts = __SLR1ParserConflicts(grammar)
    automaton = build_lr0_automaton(grammar.get_augmented_grammar(True))
    return shift_reduce_info(
        automaton,
        parser_conflicts.action,
        parser_conflicts.goto,
        __SLR1ParserConflicts.SHIFT,
        __SLR1ParserConflicts.REDUCE,
    )


@lru_cache
def is_slr_grammar(grammar):
    parser_info = __build_slr_info(grammar)
    return not any(len(v) > 1 for v in parser_info.action_table.values())


def build_slr_tables(grammar):
    parser_info = __build_slr_info(grammar)
    return parser_info.action_table, parser_info.goto_table


@lru_cache
def build_conflict_str(grammar):
    parser_info = __build_slr_info(grammar)
    return __build_conflict_str(
        parser_info.action_table,
        parser_info.goto_table,
        grammar.terminals + [grammar.eof],
        parser_info.shift_act,
        parser_info.reduce_act,
    )


@lru_cache
def build_automaton(grammar):
    parser_info = __build_slr_info(grammar)
    return parser_info.automaton.graph()


def get_derivation_tree_builder(grammar):
    parser = __build_slr_parser(grammar)

    def tree_builder(tokens):
        parse = parser([grammar[t] for t in tokens] + [grammar.eof])
        right_parse = tuple(reversed(parse))
        print(right_parse)
        return build_derivation_tree(right_parse, is_right_parse=True)

    return tree_builder


@lru_cache
def __build_slr_parser(grammar):
    return SLR1Parser(grammar)
