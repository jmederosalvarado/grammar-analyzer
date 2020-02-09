from pycmp.grammar import Grammar
from grammar_analyzer.input.ast import GNode, ProdNode, SentNode, SymbolNode


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
    symbol_list %= symbol + symbol_list, lambda h, s: [SymbolNode(s[0])] + s[1]
    symbol_list %= symbol, lambda h, s: [SymbolNode(s[0])]

    return input_grammar
