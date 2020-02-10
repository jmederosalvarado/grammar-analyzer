from grammar_analyzer.interpreter.evaluation import (
    register_nonterminals,
    register_productions,
    register_start_symbol,
    register_terminals,
)
from grammar_analyzer.interpreter.language import lexer, parser
from pycmp.evaluation import evaluate_reverse_parse
from pycmp.grammar import Grammar
from pycmp.parsing import LR1Parser


def eval_input(text):
    tokens = lexer(text)
    parse, actions = parser(tokens)
    ast = evaluate_reverse_parse(parse, actions, tokens)
    return evaluate_ast(ast)


def evaluate_ast(node):
    grammar = Grammar()
    register_start_symbol(node, grammar)
    register_nonterminals(node, grammar)
    register_terminals(node, grammar)
    register_productions(node, grammar)
    return grammar
