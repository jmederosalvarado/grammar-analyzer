from grammar_analyzer.interpreter.ast import GNode, ProdNode, SentNode, SymbolNode
from pycmp.grammar import Grammar, Production, Sentence, Symbol
from utils import visitor

# TODO: Refactor

# region Register start symbol


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


# endregion

# region Register non terminals


@visitor.on("node")
def register_nonterminals(node, grammar):
    pass


@register_nonterminals.when(GNode)
def register_nonterminals_gnode(node, grammar):
    for prod in node.productions:
        register_nonterminals(prod, grammar)


@register_nonterminals.when(ProdNode)
def register_nonterminals_prod(node, grammar):
    register_nonterminals(node.head, grammar)


@register_nonterminals.when(SymbolNode)
def register_nonterminals_symbol(node, grammar):
    if node.lex not in grammar.nonterminals:
        grammar.add_nonterminal(node.lex)


# endregion

# region Register terminals


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


# endregion

# region Register productions


@visitor.on("node")
def register_productions(node, grammar):
    pass


@register_productions.when(GNode)
def register_productions_gnode(node, grammar):
    prods = [eval_node(p, grammar) for p in node.productions]
    for prod in prods:
        grammar.add_production(prod)


# endregion

# region Evaluate nodes


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


# endregion
