import pytest

from pycmp.automata import move, epsilon_closure
from pycmp.automata import nfa_to_dfa
from pycmp.automata import automata_union, automata_concatenation, automata_closure
from pycmp.automata import state_minimization, automata_minimization
from pycmp.automata import State

from tests.pycmp_tests.test_automata_cases import test_dfa_cases
from tests.pycmp_tests.test_automata_cases import test_move_cases
from tests.pycmp_tests.test_automata_cases import test_epsilon_closure_cases
from tests.pycmp_tests.test_automata_cases import test_nfa_to_dfa_states_cases
from tests.pycmp_tests.test_automata_cases import test_nfa_to_dfa_finals_cases
from tests.pycmp_tests.test_automata_cases import test_nfa_to_dfa_recognize_cases
from tests.pycmp_tests.test_automata_cases import test_automata_union_states_cases
from tests.pycmp_tests.test_automata_cases import test_automata_union_recognize_cases
from tests.pycmp_tests.test_automata_cases import (
    test_automata_concatenation_states_cases,
)
from tests.pycmp_tests.test_automata_cases import (
    test_automata_concatenation_recognize_cases,
)
from tests.pycmp_tests.test_automata_cases import test_automata_closure_states_cases
from tests.pycmp_tests.test_automata_cases import test_automata_closure_recognize_cases
from tests.pycmp_tests.test_automata_cases import test_state_minimization_finals_cases
from tests.pycmp_tests.test_automata_cases import test_state_minimization_states_cases
from tests.pycmp_tests.test_automata_cases import test_state_minimization_group_cases
from tests.pycmp_tests.test_automata_cases import (
    test_automata_minimization_states_cases,
)
from tests.pycmp_tests.test_automata_cases import (
    test_automata_minimization_recognize_cases,
)
from tests.pycmp_tests.test_automata_cases import test_state_cases


@pytest.mark.parametrize(("dfa", "text", "recognize"), test_dfa_cases)
def test_dfa(dfa, text, recognize):
    return recognize == dfa.recognize(text)


@pytest.mark.parametrize(("nfa", "states", "symbol", "result"), test_move_cases)
def test_move(nfa, states, symbol, result):
    return result == move(nfa, states, symbol)


@pytest.mark.parametrize(("nfa", "states", "closure"), test_epsilon_closure_cases)
def test_epsilon_closure(nfa, states, closure):
    return closure == epsilon_closure(nfa, states)


@pytest.mark.parametrize(("nfa", "states"), test_nfa_to_dfa_states_cases)
def test_nfa_to_dfa_states(nfa, states):
    dfa = nfa_to_dfa(nfa)
    assert states == dfa.states


@pytest.mark.parametrize(("nfa", "finals"), test_nfa_to_dfa_finals_cases)
def test_nfa_to_dfa_finals(nfa, finals):
    dfa = nfa_to_dfa(nfa)
    assert finals == len(dfa.finals)


@pytest.mark.parametrize(("nfa", "text", "recognize"), test_nfa_to_dfa_recognize_cases)
def test_nfa_to_dfa_recognize(nfa, text, recognize):
    dfa = nfa_to_dfa(nfa)
    assert recognize == dfa.recognize(text)


@pytest.mark.parametrize(("a1", "a2", "states"), test_automata_union_states_cases)
def test_automata_union_states(a1, a2, states):
    union = automata_union(a1, a2)
    assert states == union.states


@pytest.mark.parametrize(
    ("a1", "a2", "text", "recognize"), test_automata_union_recognize_cases
)
def test_automata_union_recognize(a1, a2, text, recognize):
    union = automata_union(a1, a2)
    union = nfa_to_dfa(union)
    assert recognize == union.recognize(text)


@pytest.mark.parametrize(
    ("a1", "a2", "states"), test_automata_concatenation_states_cases
)
def test_automata_concatenation_states(a1, a2, states):
    concatenation = automata_concatenation(a1, a2)
    assert states == concatenation.states


@pytest.mark.parametrize(
    ("a1", "a2", "text", "recognize"), test_automata_concatenation_recognize_cases
)
def test_automata_concatenation_recognize(a1, a2, text, recognize):
    concatenation = automata_concatenation(a1, a2)
    concatenation = nfa_to_dfa(concatenation)
    assert recognize == concatenation.recognize(text)


@pytest.mark.parametrize(("automaton", "states"), test_automata_closure_states_cases)
def test_automata_closure_states(automaton, states):
    closure = automata_closure(automaton)
    assert states == closure.states


@pytest.mark.parametrize(
    ("automaton", "text", "recognize"), test_automata_closure_recognize_cases
)
def test_automata_closure_recognize(automaton, text, recognize):
    closure = automata_closure(automaton)
    closure = nfa_to_dfa(closure)
    assert recognize == closure.recognize(text)


@pytest.mark.parametrize(("automaton"), test_state_minimization_finals_cases)
def test_state_minimization_finals(automaton):
    states = state_minimization(automaton)

    for members in states.groups:
        all_in_finals = all(m.value in automaton.finals for m in members)
        none_in_finals = all(m.value not in automaton.finals for m in members)
        assert all_in_finals or none_in_finals


@pytest.mark.parametrize(("automaton", "states"), test_state_minimization_states_cases)
def test_state_minimization_states(automaton, states):
    assert states == len(state_minimization(automaton))


@pytest.mark.parametrize(("automaton", "group"), test_state_minimization_group_cases)
def test_state_minimization_group(automaton, group):
    states = state_minimization(automaton)
    head, *tail = group
    representative = states[head].representative
    if len(tail) == 0:
        assert representative == states[head]
    assert all(representative == states[i].representative for i in group)


@pytest.mark.parametrize(
    ("automaton", "states"), test_automata_minimization_states_cases
)
def test_automata_minimization_states(automaton, states):
    minimized = automata_minimization(automaton)
    assert states == minimized.states


@pytest.mark.parametrize(
    ("automaton", "text", "recognize"), test_automata_minimization_recognize_cases
)
def test_automata_minimization_recognize(automaton, text, recognize):
    minimized = automata_minimization(automaton)
    assert recognize == minimized.recognize(text)


@pytest.mark.parametrize(("automaton", "text", "recognize"), test_state_cases)
def test_state(automaton, text, recognize):
    state = State.from_nfa(automaton)
    assert recognize == state.recognize(text)
