import json
from grammar_analyzer.interpreter.language import grammar, lexer, parser
from grammar_analyzer.interpreter import eval_input
from pycmp.evaluation import evaluate_reverse_parse
from pycmp.token import Token
from pycmp.grammar import Grammar

# TODO: Add more tests for inputcmp


def test_build_lexer_1():
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


def gnode_to_json_repr(gnode):
    return [prod_to_json_repr(prod) for prod in gnode.productions]


def prod_to_json_repr(prod):
    print(type(prod.head))
    return {
        "head": symbol_to_json_repr(prod.head),
        "body": sent_to_json_repr(prod.body),
    }


def sent_to_json_repr(sent):
    return " ".join(symbol_to_json_repr(sym) for sym in sent.symbols)


def symbol_to_json_repr(sym):
    return sym.lex


def test_grammar_1():
    tokens = [
        Token("b", grammar["symbol"]),
        Token("->", grammar["->"]),
        Token("pa", grammar["symbol"]),
        Token("b", grammar["symbol"]),
        Token("pc", grammar["symbol"]),
        Token("$", grammar.eof),
    ]
    parse, actions = parser(tokens)
    ast = evaluate_reverse_parse(parse, actions, tokens)
    json_repr = gnode_to_json_repr(ast)
    goal = '[{"head": "b", "body": "pa b pc"}]'
    assert goal == json.dumps(json_repr)


def test_grammar_2():
    tokens = [
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
    parse, actions = parser(tokens)
    ast = evaluate_reverse_parse(parse, actions, tokens)
    json_repr = gnode_to_json_repr(ast)
    goal = '[{"head": "balanced", "body": "( balanced )"}, {"head": "balanced", "body": "balanced ( )"}, {"head": "balanced", "body": "( ) balanced"}]'
    assert goal == json.dumps(json_repr)


def test_eval_input():
    text = "balanced -> ( balanced ) | balanced ( ) | ( ) balanced | eps"
    goal_grammar = Grammar()
    balanced = goal_grammar.add_nonterminal("balanced", True)
    opar, cpar = goal_grammar.add_terminals("( )")
    balanced %= opar + balanced + cpar | balanced + opar + cpar
    balanced %= opar + cpar + balanced | goal_grammar.epsilon
    input_grammar = eval_input(text)
    assert goal_grammar.to_json == input_grammar.to_json
