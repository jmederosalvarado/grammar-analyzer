import pytest

from pycmp.regex import Regex

test_regex_cases = [
    ("a*(a|b)*cd | ε", "", True),
    ("a*(a|b)*cd | ε", "cd", True),
    ("a*(a|b)*cd | ε", "aaaaacd", True),
    ("a*(a|b)*cd | ε", "bbbbbcd", True),
    ("a*(a|b)*cd | ε", "bbabababcd", True),
    ("a*(a|b)*cd | ε", "aaabbabababcd", True),
    ("a*(a|b)*cd | ε", "cda", False),
    ("a*(a|b)*cd | ε", "aaaaa", False),
    ("a*(a|b)*cd | ε", "bbbbb", False),
    ("a*(a|b)*cd | ε", "ababba", False),
    ("a*(a|b)*cd | ε", "cdbaba", False),
    ("a*(a|b)*cd | ε", "cababad", False),
    ("a*(a|b)*cd | ε", "bababacc", False),
]


@pytest.mark.parametrize(("regex", "text", "recognize"), test_regex_cases)
def test_regex(regex, text, recognize):
    regex = Regex(regex, skip_whitespaces=True)
    assert recognize == regex(text)
