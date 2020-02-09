from grammar_analyzer.inputcmp import build_input_grammar
from grammar_analyzer.inputcmp import build_lexer
from pycmp.token import Token

# TODO: Add more tests for inputcmp


def test_build_lexer_1():
    grammar = build_input_grammar()
    lexer = build_lexer(grammar)

    tokens = lexer("b -> pa b pc")

    assert [
        Token("b", grammar["symbol"]),
        Token("->", grammar["->"]),
        Token("pa", grammar["symbol"]),
        Token("b", grammar["symbol"]),
        Token("pc", grammar["symbol"]),
        Token("$", grammar.eof),
    ] == [t for t in tokens if t.ttype is not None]


def test_build_lexer_2():
    grammar = build_input_grammar()
    lexer = build_lexer(grammar)

    tokens = lexer("balanced -> ( balanced ) | balanced ( ) | ( ) balanced")

    assert [t for t in tokens if t.ttype is not None] == [
        Token("balanced", grammar["symbol"]),
        Token("->", grammar["->"]),
        Token("(", grammar["symbol"]),
        Token("balanced", grammar["symbol"]),
        Token(")", grammar["symbol"]),
        Token("|", grammar["|"]),
        Token("balanced", grammar["symbol"]),
        Token("(", grammar["symbol"]),
        Token(")", grammar["symbol"]),
        Token("|", grammar["|"]),
        Token("(", grammar["symbol"]),
        Token(")", grammar["symbol"]),
        Token("balanced", grammar["symbol"]),
        Token("$", grammar.eof),
    ]
