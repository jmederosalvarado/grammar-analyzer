import pytest

from pycmp.parsing import compute_firsts, compute_follows
from pycmp.parsing import build_ll_table, build_ll_parser
from pycmp.evaluation import evaluate_parse

from tests.pycmp_tests.test_parsing_cases import test_compute_firsts_cases
from tests.pycmp_tests.test_parsing_cases import test_compute_follows_cases
from tests.pycmp_tests.test_parsing_cases import test_build_ll_table_cases
from tests.pycmp_tests.test_parsing_cases import test_build_ll_parser_cases
from tests.pycmp_tests.test_parsing_cases import test_evaluate_parse_cases


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
