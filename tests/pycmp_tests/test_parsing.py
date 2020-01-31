import pytest

from pycmp.parsing import compute_firsts, compute_follows
from pycmp.parsing import build_ll_table, build_ll_parser
from pycmp.parsing import build_lr0_automaton, build_lr1_automaton
from pycmp.parsing import expand, closure_lr1, goto_lr1
from pycmp.parsing import SLR1Parser, LR1Parser
from pycmp.evaluation import evaluate_parse

from tests.pycmp_tests.test_parsing_cases import test_compute_firsts_cases
from tests.pycmp_tests.test_parsing_cases import test_compute_follows_cases
from tests.pycmp_tests.test_parsing_cases import test_build_ll_table_cases
from tests.pycmp_tests.test_parsing_cases import test_build_ll_parser_cases
from tests.pycmp_tests.test_parsing_cases import test_evaluate_parse_cases
from tests.pycmp_tests.test_parsing_cases import test_build_lr0_automaton_cases
from tests.pycmp_tests.test_parsing_cases import test_build_lr1_automaton_cases
from tests.pycmp_tests.test_parsing_cases import test_slr1_parser_cases
from tests.pycmp_tests.test_parsing_cases import test_expand_cases
from tests.pycmp_tests.test_parsing_cases import test_closure_lr1_cases
from tests.pycmp_tests.test_parsing_cases import test_goto_lr1_cases
from tests.pycmp_tests.test_parsing_cases import test_lr1_parser_cases


@pytest.mark.parametrize(('grammar', 'firsts'), test_compute_firsts_cases)
def test_compute_first(grammar, firsts):
    assert firsts == compute_firsts(grammar)


@pytest.mark.parametrize(('grammar', 'firsts', 'follows'), test_compute_follows_cases)
def test_compute_follows(grammar, firsts, follows):
    assert follows == compute_follows(grammar, firsts)


@pytest.mark.parametrize(('grammar', 'firsts', 'follows', 'table'), test_build_ll_table_cases)
def test_build_ll_table(grammar, firsts, follows, table):
    assert table == build_ll_table(grammar, firsts, follows)


@pytest.mark.parametrize(('grammar', 'firsts', 'follows', 'table', 'tokens', 'parse'), test_build_ll_parser_cases)
def test_build_ll_parser(grammar, firsts, follows, table, tokens, parse):
    parser = build_ll_parser(grammar, table, firsts, follows)
    assert parse == parser(tokens)


@pytest.mark.parametrize(('left_parse', 'tokens', 'result'), test_evaluate_parse_cases)
def test_evaluate_parse(left_parse, tokens, result):
    assert result == evaluate_parse(left_parse, tokens)


@pytest.mark.parametrize(('grammar', 'text', 'recognize'), test_build_lr0_automaton_cases)
def test_build_lr0_automaton(grammar, text, recognize):
    automaton = build_lr0_automaton(grammar)
    assert recognize == automaton.recognize(text)


@pytest.mark.parametrize(('grammar', 'tokens', 'derivation'), test_slr1_parser_cases)
def test_slr1_parser(grammar, tokens, derivation):
    parser = SLR1Parser(grammar)
    assert derivation == str(parser(tokens))


@pytest.mark.parametrize(('item', 'firsts', 'result'), test_expand_cases)
def test_expand(item, firsts, result):
    assert result == str(expand(item, firsts))


@pytest.mark.parametrize(('items', 'firsts', 'expected'), test_closure_lr1_cases)
def test_closure_lr1(items, firsts, expected):
    assert expected == closure_lr1(items, firsts)


@pytest.mark.parametrize(('items', 'symbol', 'firsts', 'expected'), test_goto_lr1_cases)
def test_goto_lr1(items, symbol, firsts, expected):
    assert expected == goto_lr1(items, symbol, firsts)


@pytest.mark.parametrize(('grammar', 'text', 'recognize'), test_build_lr1_automaton_cases)
def test_build_lr1_automaton(grammar, text, recognize):
    automaton = build_lr1_automaton(grammar)
    assert recognize == automaton.recognize(text)


@pytest.mark.parametrize(('grammar', 'tokens', 'derivation'), test_lr1_parser_cases)
def test_lr1_parser(grammar, tokens, derivation):
    parser = LR1Parser(grammar, verbose=True)
    assert derivation == str(parser(tokens))
