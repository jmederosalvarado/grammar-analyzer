import pytest

from pycmp.lexer import Lexer

from tests.pycmp_tests.test_lexer_cases import test_lexer_lex_cases
from tests.pycmp_tests.test_lexer_cases import test_lexer_ttype_cases


@pytest.mark.parametrize(("regexs", "eof", "text", "lexs"), test_lexer_lex_cases)
def test_lexer_lexs(regexs, eof, text, lexs):
    lexer = Lexer(regexs, eof)
    tokens = lexer(text)
    print(f"{tokens=}")
    assert lexs == tuple(t.lex for t in tokens)


@pytest.mark.parametrize(("regexs", "eof", "text", "ttypes"), test_lexer_ttype_cases)
def test_lexer_ttypes(regexs, eof, text, ttypes):
    lexer = Lexer(regexs, eof)
    tokens = lexer(text)
    assert ttypes == tuple(t.ttype for t in tokens)
