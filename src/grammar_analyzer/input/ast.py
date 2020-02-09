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
