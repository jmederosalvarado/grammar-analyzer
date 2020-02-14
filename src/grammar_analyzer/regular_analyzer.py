from pycmp.automata import NFA


def automaton_to_regex(automaton: NFA) -> str:
    states, transitions = to_gnfa(automaton)
    return gnfa_to_regex(list(range(states)), transitions)


def gnfa_to_regex(states: list, transitions: dict) -> str:
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
            transitions[qi, qj] = f"(({r1})({r2})*({r3}))|({r4})"

    return gnfa_to_regex(states, transitions)


def to_gnfa(automaton: NFA) -> tuple:
    start, old_start = 0, 1
    final = automaton.states + old_start
    states = automaton.states + 2

    transitions = {}
    for origin in range(automaton.states):
        for dest in range(automaton.states):
            trans_syms = []
            for symbol in automaton.vocabulary:
                dests = automaton.transitions[origin].get(symbol)
                if dests is not None and dest in dests:
                    trans_syms.append(symbol)
            trans_regex = "<nosymbol>" if not trans_syms else "|".join(trans_syms)
            transitions[old_start + origin, old_start + dest] = trans_regex

    ## Add transitions from start state ...
    transitions[start, old_start] = ""
    for state in automaton.states:
        transitions[start, state] = "<nosymbol>"

    ## Add transitions to final state ...
    for state in automaton.states:
        symbol = "" if state in automaton.finals else "<nosymbol>"
        transitions[old_start + state, final] = symbol

    return states, transitions

