from pycmp.grammar import Grammar
from pycmp.ast import Node
from pycmp.lexer import Lexer


class GNode(object):
    def __init__(self, productions):
        self.productions = tuple(productions)


class ProdNode(object):
    def __init__(self, left, right):
        self.left = left
        self.right = tuple(right)


class SentNode(object):
    def __init__(self, symbols):
        self.symbols = tuple(symbols)


class SymbolNode(object):
    def __init__(self, lex):
        self.lex = lex


def build_input_grammar():
    """
    Returns the following grammar:

    grammar -> prod_list
    prod_list -> prod | prod prod_list
    prod -> symbol '->' sent_list
    sent_list -> sent | sent '|' sent_list
    sent -> symbol_list | 'eps'
    symbol_list -> symbol | symbol symbol_list
    """
    input_grammar = Grammar()
    grammar = input_grammar.add_nonterminal('grammar', True)
    prod, prod_list = input_grammar.add_nonterminals('prod prod_list')
    sent, sent_list, symbol_list = input_grammar.add_nonterminals('sent sent_list symbol_list')
    symbol, arrow, union, eps, eol = input_grammar.add_terminals('symbol -> | eps eol')

    grammar %= prod_list, lambda h, s: GNode(s[0])
    prod_list %= prod + eol + prod_list, lambda h, s: [s[0]] + s[1]
    prod_list %= prod, lambda h, s: [s[0]]
    prod %= symbol + arrow + sent_list, lambda h, s: ProdNode(s[0], s[2])
    sent_list %= sent + union + sent_list, lambda h, s: lambda h, s: [s[0]] + s[2]
    sent_list %= sent, lambda h, s: [s[0]]
    sent %= symbol_list, lambda h, s: SentNode(s[0])
    sent %= eps, lambda h, s: SentNode([s[0]])
    symbol_list %= symbol + symbol_list, lambda h, s: [s[0]] + s[1]
    symbol_list %= symbol, lambda h, s: [s[0]]

    return input_grammar


def build_lexer(grammar):
    digits = '|'.join(str(n) for n in range(10))
    letters = '|'.join(chr(n) for n in range(ord('a'), ord('z')+1))
    return Lexer([
        (grammar['eps'], 'eps'),
        (grammar['|'], r'\|'),
        (grammar['->'], '->'),
        (grammar['eol'], '\\n'),
        (None, '  *'),
        (grammar['symbol'], f'({letters}|{digits})*')
    ], grammar.eof)
