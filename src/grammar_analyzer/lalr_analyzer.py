from functools import lru_cache
from itertools import chain
from pycmp.parsing import ShiftReduceParser, build_lr1_automaton
from pycmp.automata import State
from pycmp.grammar import Item
from grammar_analyzer.shift_reduce_analyzer import (
    shift_reduce_info,
    build_conflict_str as __build_conflict_str,
)
from grammar_analyzer.common import build_derivation_tree


def merge_items_lookaheads(items, others):
    if len(items) != len(others):
        return False

    new_lookaheads = []
    for item in items:
        for item2 in others:
            if item.center() == item2.center():
                new_lookaheads.append(item2.lookaheads)
                break
        else:
            return False

    for item, new_lookahead in zip(items, new_lookaheads):
        item.lookaheads = item.lookaheads.union(new_lookahead)

    return True


def build_lalr_automaton(G):
    lr1_automaton = build_lr1_automaton(G)
    states = list(lr1_automaton)
    new_states = []
    visited = {}

    for i, state in enumerate(states):
        if state not in visited:
            # creates items
            items = [item.center() for item in state.state]

            # check for states with same center
            for state2 in states[i:]:
                if merge_items_lookaheads(items, state2.state):
                    visited[state2] = len(new_states)

            # add new state
            new_states.append(State(frozenset(items), True))

    # making transitions
    for state in states:
        new_state = new_states[visited[state]]
        for symbol, transitions in state.transitions.items():
            for state2 in transitions:
                new_state2 = new_states[visited[state2]]
                # check if the transition already exists
                if (
                    symbol not in new_state.transitions
                    or new_state2 not in new_state.transitions[symbol]
                ):
                    new_state.add_transition(symbol, new_state2)

    return new_states[0]


class LALRParser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.Augmented = self.grammar.get_augmented_grammar(True)

        automaton = self.automaton = build_lalr_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i
            node.tag = f"I{i}"

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.is_reduce_item:
                    prod = item.production
                    if prod.left == G.start_symbol:
                        self._register(self.action, (idx, G.eof), (self.OK, ""))
                    else:
                        for lookahead in item.lookaheads:
                            self._register(
                                self.action, (idx, lookahead), (self.REDUCE, prod),
                            )
                else:
                    next_symbol = item.next_symbol
                    if next_symbol.is_terminal:
                        self._register(
                            self.action,
                            (idx, next_symbol),
                            (self.SHIFT, node[next_symbol.name][0].idx),
                        )
                    else:
                        self._register(
                            self.goto, (idx, next_symbol), node[next_symbol.name][0].idx
                        )

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
            table[key] = [value]


@lru_cache
def __build_lalr_info(grammar):
    parser_conflicts = __LALRParserConflicts(grammar)
    automaton = build_lr1_automaton(grammar.get_augmented_grammar(True))
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
        grammar.terminals + [grammar.eof],
        parser_info.shift_act,
        parser_info.reduce_act,
    )


@lru_cache
def build_automaton(grammar):
    parser_info = __build_lalr_info(grammar)
    return parser_info.automaton.graph()


def get_derivation_tree_builder(grammar):
    parser = __build_lalr_parser(grammar)

    def tree_builder(tokens):
        parse = parser(tokens)
        right_parse = reversed(parse)
        return build_derivation_tree(right_parse, is_right_parse=True)

    return tree_builder


@lru_cache
def __build_lalr_parser(grammar):
    return LALRParser(grammar)
