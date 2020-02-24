from functools import lru_cache
from itertools import chain
from pycmp.parsing import ShiftReduceParser, build_lr1_automaton
from pycmp.grammar import Item
from grammar_analyzer.shift_reduce_analyzer import (
    shift_reduce_info,
    build_conflict_str as __build_conflict_str,
)
from grammar_analyzer.common import build_derivation_tree

# TODO: Refactor all shift-reduce analyzers to share common code


class LALRParser(ShiftReduceParser):
    def _build_parsing_table(self):
        """
        Method to construct an LALR parser:
        1. Construct C = (Io, 11, ... , I,), the collection of sets of LR(1) items. 
        2. For each core present among the set of LR(1) items, find all sets having
           that core, and replace these sets by their union.
        3. Let C' = {Jo, J1,... , J,) be the resulting sets of LR(1) items. The
           parsing actions for state i are constructed from Ji in the same manner as
           in LR. If there is a parsing action conflict, the algorithm fails
           to produce a parser, and the grammar is said not to be LALR(1).
        4. The GOTO table is constructed as follows. If J is the union of one or
           more sets of LR(1) items, that is, J = Il n I2 n ... n Ik, then the
           cores of GOTO(I1, X) , GOTO(I2, X) , ... , GOTO(Ik, X) are the same, since
           11, 12, ... , Ik all have the same core. Let K be the union of all sets of
           items having the same core as GOTO(I1, X). Then GOTO(J, X) = K. 
        """
        grammar = self.grammar.get_augmented_grammar(True)

        automaton = build_lr1_automaton(grammar)
        merged_states = self._merge_states(node.state for node in automaton)

        for idx, state in enumerate(merged_states):
            for item in state:
                if item.is_reduce_item:
                    is_start = item.production.left == grammar.start_symbol
                    for s in item.lookaheads:
                        action = (
                            self.OK if is_start and s == grammar.eof else self.REDUCE
                        )
                        self._register(self.action, (idx, s), (action, item.production))
                    continue

                x = item.next_symbol
                try:
                    # TODO: Fix this
                    # dest = node.transitions[x.name][0]
                    dest = next(iter(automaton))
                except KeyError:
                    continue
                if x.is_terminal:
                    self._register(self.action, (idx, x), (self.SHIFT, dest.idx))
                else:
                    self._register(self.goto, (idx, x), dest.idx)

    @staticmethod
    def _merge_states(states):
        def get_core(state):
            return frozenset(i.center() for i in state)

        cores, new_states = frozenset(get_core(s) for s in states), []
        for core in cores:
            items = chain(state for state in states if get_core(state) == core)
            new_state = frozenset(
                Item(
                    center.production,
                    center.pos,
                    lookaheads=chain(
                        item.lookaheads for item in items if item.center() == center
                    ),
                )
                for center in core
            )
            new_states.append(new_state)

        return new_states

    @staticmethod
    def _register(table, key, value):
        assert (
            key not in table or table[key] == value
        ), "Shift-Reduce or Reduce-Reduce conflict!!!"
        table[key] = value


class __LALRParserConflicts(LALRParser):
    def __call__(self, tokens, return_actions=False):
        raise NotImplementedError()

    @staticmethod
    def _register(table, key, value):
        if key in table and value not in table[key]:
            table[key].append(value)
        else:
            table[key].append(value)


@lru_cache
def __build_lalr_info(grammar):
    parser_conflicts = __LALRParserConflicts(grammar)
    automaton = build_lr1_automaton(grammar)
    return shift_reduce_info(
        automaton,
        parser_conflicts.action,
        parser_conflicts.goto,
        __LALRParserConflicts.SHIFT,
        __LALRParserConflicts.REDUCE,
    )


@lru_cache
def is_lalr_grammar(grammar):
    parser_info = __build_lalr_info(grammar)
    return not any(len(v) > 1 for v in parser_info.action_table.values())


def build_lalr_tables(grammar):
    parser_info = __build_lalr_info(grammar)
    return parser_info.action_table, parser_info.goto_table


@lru_cache
def build_conflict_str(grammar):
    parser_info = __build_lalr_info(grammar)
    return __build_conflict_str(
        parser_info.action_table,
        parser_info.goto_table,
        grammar.terminals,
        parser_info.shift_act,
        parser_info.reduce_act,
    )


@lru_cache
def build_automaton(grammar):
    parser_info = __build_lalr_info(grammar)
    return parser_info.automaton.graph()


def get_derivation_tree_builder(grammar):
    parser = __build_lalr_parser(grammar)

    @lru_cache
    def tree_builder(tokens):
        parse = parser(tokens)
        right_parse = reversed(parse)
        return build_derivation_tree(right_parse, is_right_parse=True)

    return tree_builder


@lru_cache
def __build_lalr_parser(grammar):
    return LALRParser(grammar)
