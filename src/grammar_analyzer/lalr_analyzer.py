from functools import lru_cache
from pycmp.parsing import LR1Parser, build_lr1_automaton
from grammar_analyzer.shift_reduce_analyzer import (
    shift_reduce_info,
    build_conflict_str as __build_conflict_str,
)
from grammar_analyzer.common import build_derivation_tree

# TODO: Refactor all shift-reduce analyzers to share common code


class __LR1ParserConflicts(LR1Parser):
    def __call__(self, tokens, return_actions=False):
        raise NotImplementedError()

    @staticmethod
    def _register(table, key, value):
        if key in table and value not in table[key]:
            table[key].append(value)
        else:
            table[key].append(value)


@lru_cache
def __build_lr_info(grammar):
    parser_conflicts = __LR1ParserConflicts(grammar)
    automaton = build_lr1_automaton(grammar)
    return shift_reduce_info(
        automaton,
        parser_conflicts.action,
        parser_conflicts.goto,
        __LR1ParserConflicts.SHIFT,
        __LR1ParserConflicts.REDUCE,
    )


@lru_cache
def is_lr_grammar(grammar):
    parser_info = __build_lr_info(grammar)
    return not any(len(v) > 1 for v in parser_info.action_table.values())


def build_lr_tables(grammar):
    parser_info = __build_lr_info(grammar)
    return parser_info.action_table, parser_info.goto_table


@lru_cache
def build_conflict_str(grammar):
    parser_info = __build_lr_info(grammar)
    return __build_conflict_str(
        parser_info.action_table,
        parser_info.goto_table,
        grammar.terminals,
        parser_info.shift_act,
        parser_info.reduce_act,
    )


@lru_cache
def build_automaton(grammar):
    parser_info = __build_lr_info(grammar)
    return parser_info.automaton.graph()


def get_derivation_tree_builder(grammar):
    parser = __build_lr_parser(grammar)

    @lru_cache
    def tree_builder(tokens):
        parse = parser(tokens)
        right_parse = reversed(parse)
        return build_derivation_tree(right_parse, is_right_parse=True)

    return tree_builder


@lru_cache
def __build_lr_parser(grammar):
    return LR1Parser(grammar)
