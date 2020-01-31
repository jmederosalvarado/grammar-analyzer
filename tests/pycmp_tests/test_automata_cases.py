from pycmp.automata import DFA, NFA

automaton = DFA(states=3, finals=[2], transitions={
    (0, 'a'): 0,
    (0, 'b'): 1,
    (1, 'a'): 2,
    (1, 'b'): 1,
    (2, 'a'): 0,
    (2, 'b'): 1,
})

test_dfa_cases = [
    (automaton, 'ba', True),
    (automaton, 'aababbaba', True),
    (automaton, '', False),
    (automaton, 'aabaa', False),
    (automaton, 'aababb', False),
]

automaton = NFA(states=6, finals=[3, 5], transitions={
    (0, ''): [1, 2],
    (1, ''): [3],
    (1, 'b'): [4],
    (2, 'a'): [4],
    (3, 'c'): [3],
    (4, ''): [5],
    (5, 'd'): [5]
})

test_move_cases = [
    (automaton, [1], 'a', set()),
    (automaton, [2], 'a', {4}),
    (automaton, [1, 5], 'd', {5})
]

test_epsilon_closure_cases = [
    (automaton, [0], {0, 1, 2, 3}),
    (automaton, [0, 4], {0, 1, 2, 3, 4, 5}),
    (automaton, [1, 2, 4], {1, 2, 3, 4, 5})
]

test_nfa_to_dfa_states_cases = [(automaton, 4)]

test_nfa_to_dfa_finals_cases = [(automaton, 4)]

test_nfa_to_dfa_recognize_cases = [
    (automaton, '', True),
    (automaton, 'a', True),
    (automaton, 'b', True),
    (automaton, 'cccccc', True),
    (automaton, 'adddd', True),
    (automaton, 'bdddd', True),

    (automaton, 'dddddd', False),
    (automaton, 'cdddd', False),
    (automaton, 'aa', False),
    (automaton, 'ab', False),
    (automaton, 'ddddc', False)
]

automaton = NFA(states=3, finals=[2], transitions={
    (0, 'a'): [0],
    (0, 'b'): [0, 1],
    (1, 'a'): [2],
    (1, 'b'): [2],
})

test_move_cases += [
    (automaton, [0, 1], 'a', {0, 2}),
    (automaton, [0, 1], 'b', {0, 1, 2})
]

test_nfa_to_dfa_states_cases += [(automaton, 4)]

test_nfa_to_dfa_finals_cases += [(automaton, 2)]

test_nfa_to_dfa_recognize_cases += [
    (automaton, 'aba', True),
    (automaton, 'bb', True),
    (automaton, 'aaaaaaaaaaaba', True),

    (automaton, 'aaa', False),
    (automaton, 'ab', False),
    (automaton, 'b', False),
    (automaton, '', False)
]

automaton = NFA(states=5, finals=[4], transitions={
    (0, 'a'): [0, 1],
    (0, 'b'): [0, 2],
    (0, 'c'): [0, 3],
    (1, 'a'): [1, 4],
    (1, 'b'): [1],
    (1, 'c'): [1],
    (2, 'a'): [2],
    (2, 'b'): [2, 4],
    (2, 'c'): [2],
    (3, 'a'): [3],
    (3, 'b'): [3],
    (3, 'c'): [3, 4],
})

test_move_cases += [
    (automaton, [0, 1], 'a', {0, 2}),
    (automaton, [0, 1], 'b', {0, 1, 2})
]

test_nfa_to_dfa_states_cases += [(automaton, 15)]

test_nfa_to_dfa_finals_cases += [(automaton, 7)]

test_nfa_to_dfa_recognize_cases += [
    (automaton, 'abccac', True),
    (automaton, 'bbbbbbbbaa', True),
    (automaton, 'cac', True),

    (automaton, 'abbbbc', False),
    (automaton, 'a', False),
    (automaton, '', False),
    (automaton, 'acacacaccab', False)
]

automaton = DFA(states=2, finals=[1], transitions={
    (0, 'a'):  0,
    (0, 'b'):  1,
    (1, 'a'):  0,
    (1, 'b'):  1,
})

test_automata_union_states_cases = [
    (automaton, automaton, 2*automaton.states + 2)
]

test_automata_union_recognize_cases = [
    (automaton, automaton, 'b', True),
    (automaton, automaton, 'abbb', True),
    (automaton, automaton, 'abaaababab', True),

    (automaton, automaton, '', False),
    (automaton, automaton, 'a', False),
    (automaton, automaton, 'abbbbaa', False)
]

test_automata_concatenation_states_cases = [
    (automaton, automaton, 2*automaton.states + 1)
]

test_automata_concatenation_recognize_cases = [
    (automaton, automaton, 'bb', True),
    (automaton, automaton, 'abbb', True),
    (automaton, automaton, 'abaaababab', True),

    (automaton, automaton, '', False),
    (automaton, automaton, 'a', False),
    (automaton, automaton, 'b', False),
    (automaton, automaton, 'aaaab', False),
    (automaton, automaton, 'abbbbaa', False)
]

test_automata_closure_states_cases = [
    (automaton, automaton.states + 2)
]

test_automata_closure_recognize_cases = [
    (automaton, '', True),
    (automaton, 'b', True),
    (automaton, 'ab', True),
    (automaton, 'bb', True),
    (automaton, 'abbb', True),
    (automaton, 'abaaababab', True),

    (automaton, 'a', False),
    (automaton, 'abbbbaa', False)
]

automaton = DFA(states=5, finals=[4], transitions={
    (0, 'a'): 1,
    (0, 'b'): 2,
    (1, 'a'): 1,
    (1, 'b'): 3,
    (2, 'a'): 1,
    (2, 'b'): 2,
    (3, 'a'): 1,
    (3, 'b'): 4,
    (4, 'a'): 1,
    (4, 'b'): 2,
})

test_state_minimization_finals_cases = [(automaton)]

test_state_minimization_states_cases = [
    (automaton, 4)
]

test_state_minimization_group_cases = [
    (automaton, (0, 2)),
    (automaton, (1,)),
    (automaton, (3,)),
    (automaton, (4,))
]

test_automata_minimization_states_cases = [
    (automaton, 4)
]

test_automata_minimization_recognize_cases = [
    (automaton, 'abb', True),
    (automaton, 'ababbaabb', True),

    (automaton, '', False),
    (automaton, 'ab', False),
    (automaton, 'aaaaa', False),
    (automaton, 'abaaababab', False),
    (automaton, 'bbbbb', False),
    (automaton, 'abbabababa', False)
]

automaton = DFA(states=3, finals=[2], transitions={
    (0, 'a'): 0,
    (0, 'b'): 1,
    (1, 'a'): 2,
    (1, 'b'): 1,
    (2, 'a'): 0,
    (2, 'b'): 1,
})

test_state_cases = [
    (automaton, 'ba', True),
    (automaton, 'aababbaba', True),
    (automaton, '', False),
    (automaton, 'aabaa', False),
    (automaton, 'aababb', False)
]
