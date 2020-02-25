from pycmp.grammar import Grammar
from pycmp.automata import NFA, DFA, nfa_to_dfa


def is_regular_grammar(grammar):
    for _, right in grammar.productions:
        if not right[0].is_terminal:
            return False
        if len(right) >= 2 and not right[1].is_nonterminal:
            return False
        if len(right) > 2:
            return False
    return True


def grammar_to_automaton(grammar):
    nonterminals = (nt for nt in grammar.nonterminals
                    if nt != grammar.start_symbol)
    state_map = {nt: i + 1 for i, nt in enumerate(nonterminals)}
    state_map[grammar.start_symbol] = 0

    states = len(grammar.nonterminals) + 1
    final = states - 1
    transitions = {}

    for left, right in grammar.productions:
        origin = state_map[left]
        symbol = right[0].name

        dest = state_map[right[1]] if len(right) == 2 else final
        try:
            if not dest in transitions[origin, symbol]:
                transitions[origin, symbol].append(dest)
        except KeyError:
            transitions[origin, symbol] = [dest]

    return NFA(states, {final}, transitions)


def automaton_to_regex(automaton):
    automaton = nfa_to_dfa(automaton)

    states, transitions = __automaton_to_gnfa(automaton)
    return __gnfa_to_regex(list(range(states)), transitions)


def __gnfa_to_regex(states, transitions):
    if len(states) == 2:
        return transitions[states[0], states[-1]]

    # remove state
    qrip = states.pop(1)
    for qi in states[:-1]:
        for qj in states[1:]:
            r1, r2, r3, r4 = (
                transitions[qi, qrip],
                transitions[qrip, qrip],
                transitions[qrip, qj],
                transitions[qi, qj],
            )
            if r1 == "":
                r1 = "ε"
            if r1 == "<nosymbol>":
                r1 = ""

            if r2 == "":
                r2 = "ε"
            if r2 == "<nosymbol>":
                r2 = ""

            if r3 == "":
                r3 = "ε"
            if r3 == "<nosymbol>":
                r3 = ""

            if r4 == "":
                r4 = "ε"
            if r4 == "<nosymbol>":
                r4 = ""

            r1 = f"({r1})" if len(r1) > 1 else r1
            r2 = f"({r2})" if len(r2) > 1 else r2
            r3 = f"({r3})" if len(r3) > 1 else r3
            r4 = f"({r4})" if len(r4) > 1 else r4
            r1r2 = f"{r1}{r2}*" if r1 or r2 else ""
            r1r2r3 = f"({r1r2}{r3})" if r1r2 else r3
            transitions[qi,
                        qj] = f"{r1r2r3}|{r4}" if r1r2r3 and r4 else (r1r2r3
                                                                      or r4)

    return __gnfa_to_regex(states, transitions)


def __automaton_to_gnfa(automaton):
    start, old_start = 0, 1
    states = automaton.states + 2
    final = states - 1

    transitions = {}
    for origin in range(automaton.states):
        for dest in range(automaton.states):
            trans_syms = []
            for symbol in automaton.vocabulary:
                dests = automaton.transitions[origin].get(symbol)
                if dests is not None and dest in dests:
                    trans_syms.append(symbol)
            trans_regex = "<nosymbol>" if not trans_syms else "|".join(
                trans_syms)
            transitions[old_start + origin, old_start + dest] = trans_regex

    ## Add transitions from start state ...
    transitions[start, old_start] = ""
    for state in range(automaton.states):
        transitions[start, old_start + state] = "<nosymbol>"
    transitions[start, final] = "<nosymbol>"

    ## Add transitions to final state ...
    for state in range(automaton.states):
        symbol = "" if state in automaton.finals else "<nosymbol>"
        transitions[old_start + state, final] = symbol

    return states, transitions
