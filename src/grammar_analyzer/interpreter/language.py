from pycmp.grammar import Grammar
from pycmp.lexer import Lexer
from pycmp.parsing import LR1Parser


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


class EpsNode(SymbolNode):
    def __init__(self, lex):
        self.lex = None


def build_input_lexer(eps, union, arrow, eol, symbol, eof):
    digits = "|".join(str(n) for n in range(10))
    letters = "|".join(chr(n) for n in range(ord("a"), ord("z") + 1))
    others = "|".join([r"\(", r"\)"])
    symbols = f"{letters}|{digits}|{others}"
    ignore = "__ignore__"

    lexer = Lexer(
        [
            (eps, "eps"),
            (union, r"\|"),
            (arrow, "->"),
            (eol, "\\n"),
            (ignore, "  *"),
            (symbol, f"({symbols})({symbols})*"),
        ],
        eof,
    )

    return lambda text: [t for t in lexer(text) if t.ttype != ignore]


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

    grammar %= prod_list, lambda h, s: GNode(s[1])
    prod_list %= prod + eol + prod_list, lambda h, s: s[1] + s[2]
    prod_list %= prod, lambda h, s: s[1]
    prod %= (
        symbol + arrow + sent_list,
        lambda h, s: [ProdNode(SymbolNode(s[1]), i) for i in s[3]],
    )
    sent_list %= sent + union + sent_list, lambda h, s: [s[1]] + s[3]
    sent_list %= sent, lambda h, s: [s[1]]
    sent %= symbol_list, lambda h, s: SentNode(s[1])
    sent %= eps, lambda h, s: SentNode([EpsNode(s[1])])
    symbol_list %= symbol + symbol_list, lambda h, s: [SymbolNode(s[1])] + s[2]
    symbol_list %= symbol, lambda h, s: [SymbolNode(s[1])]

    return input_grammar


def build_input_parser(grammar):
    parser = LR1Parser(grammar)
    return lambda tokens: parser([t.ttype for t in tokens], return_actions=True)


grammar = build_input_grammar()
lexer = build_input_lexer(
    eps=grammar["eps"],
    union=grammar["|"],
    arrow=grammar["->"],
    eol=grammar["eol"],
    symbol=grammar["symbol"],
    eof=grammar.eof,
)
parser = build_input_parser(grammar)
