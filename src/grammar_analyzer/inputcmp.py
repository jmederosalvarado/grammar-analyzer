from itertools import islice
from pycmp.grammar import Grammar, Production, Symbol, Sentence
from pycmp.ast import Node
from pycmp.lexer import Lexer
from utils import visitor


class GNode(object):
    def __init__(self, productions):
        self.productions = tuple(productions)


class ProdNode(object):
    def __init__(self, head, body):
        self.head = head
        self.body = body


class SentNode(object):
    def __init__(self, symbols):
        self.symbols = tuple(symbols)


class SymbolNode(object):
    def __init__(self, lex):
        self.lex = lex


def evaluate(node):
    grammar = Grammar()
    register_start_symbol(node, grammar)
    register_nonterminals(node, grammar)
    register_terminals(node, grammar)
    register_productions(node, grammar)
    return grammar


@visitor.on("node")
def register_start_symbol(node, grammar):
    pass


@register_start_symbol.when(GNode)
def register_start_symbol_gnode(node, grammar):
    register_start_symbol(node.productions[0], grammar)


@register_start_symbol.when(ProdNode)
def register_start_symbol_prod(node, grammar):
    register_start_symbol(node.head, grammar)


@register_start_symbol.when(SymbolNode)
def register_start_symbol_symbol(node, grammar):
    grammar.add_nonterminal(node.lex, True)


@visitor.on("node")
def register_nonterminals(node, grammar):
    pass


@register_nonterminals.when(GNode)
def register_nonterminals_gnode(node, grammar):
    for prod in islice(node.productions, 1):
        register_nonterminals(prod, grammar)


@register_nonterminals.when(ProdNode)
def register_nonterminals_prod(node, grammar):
    register_nonterminals(node.head, grammar)


@register_nonterminals.when(SymbolNode)
def register_nonterminals_symbol(node, grammar):
    grammar.add_nonterminal(node.lex)


@visitor.on("node")
def register_terminals(node, grammar):
    pass


@register_terminals.when(GNode)
def register_terminals_gnode(node, grammar):
    for prod in node.productions:
        register_terminals(prod, grammar)


@register_terminals.when(ProdNode)
def register_terminals_prod(node, grammar):
    register_terminals(node.body, grammar)


@register_terminals.when(SentNode)
def register_terminals_sent(node, grammar):
    for symbol in node.symbols:
        register_terminals(symbol, grammar)


@register_terminals.when(SymbolNode)
def register_terminals_symbol(node, grammar):
    if node.lex not in grammar.nonterminals:
        grammar.add_terminal(node.lex)


@visitor.on("node")
def register_productions(node, grammar):
    pass


@register_productions.when(GNode)
def register_productions_gnode(node, grammar):
    prods = [eval_node(p, grammar) for p in node.productions]
    for prod in prods:
        grammar.add_production(prod)


@visitor.on("node")
def eval_node(node, grammar):
    pass


@eval_node.when(ProdNode)
def eval_node_prod(node, grammar):
    head = eval_node(node.head, grammar)
    body = eval_node(node.body, grammar)
    return Production(head, body)


@eval_node.when(SentNode)
def eval_node_sent(node, grammar):
    symbols = [eval_node(s, grammar) for s in node.symbols]
    return Sentence(*symbols)


@eval_node.when(SymbolNode)
def eval_node_symbol(node, grammar):
    return grammar[node.lex]


def build_input_grammar():
    """
    Returns the following grammar:

    grammar -> prod_list
    prod_list -> prod | prod eol prod_list
    prod -> symbol '->' sent_list
    sent_list -> sent | sent '|' sent_list
    sent -> symbol_list | 'eps'
    symbol_list -> symbol | symbol symbol_list
    """
    input_grammar = Grammar()
    grammar = input_grammar.add_nonterminal("grammar", True)
    prod, prod_list = input_grammar.add_nonterminals("prod prod_list")
    sent, sent_list, symbol_list = input_grammar.add_nonterminals(
        "sent sent_list symbol_list"
    )
    symbol, arrow, union, eps, eol = input_grammar.add_terminals("symbol -> | eps eol")

    grammar %= prod_list, lambda h, s: GNode(s[0])
    prod_list %= prod + eol + prod_list, lambda h, s: s[0] + s[1]
    prod_list %= prod, lambda h, s: s[0]
    prod %= symbol + arrow + sent_list, lambda h, s: [ProdNode(s[0], i) for i in s[2]]
    sent_list %= sent + union + sent_list, lambda h, s: lambda h, s: [s[0]] + s[2]
    sent_list %= sent, lambda h, s: [s[0]]
    sent %= symbol_list, lambda h, s: SentNode(s[0])
    sent %= eps, lambda h, s: SentNode([s[0]])
    symbol_list %= symbol + symbol_list, lambda h, s: [s[0]] + s[1]
    symbol_list %= symbol, lambda h, s: [s[0]]

    return input_grammar


def build_lexer(grammar):
    digits = "|".join(str(n) for n in range(10))
    letters = "|".join(chr(n) for n in range(ord("a"), ord("z") + 1))
    others = "|".join([r"\(", r"\)"])
    symbols = f"{letters}|{digits}|{others}"
    return Lexer(
        [
            (grammar["eps"], "eps"),
            (grammar["|"], r"\|"),
            (grammar["->"], "->"),
            (grammar["eol"], "\\n"),
            (None, "  *"),
            (grammar["symbol"], f"({symbols})({symbols})*"),
        ],
        grammar.eof,
    )
