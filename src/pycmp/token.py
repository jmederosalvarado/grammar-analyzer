class Token:
    def __init__(self, lex, ttype):
        self.lex = lex
        self.ttype = ttype

    def __str__(self):
        return f'{self.ttype}: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def is_valid(self):
        return True


class UnknownToken(Token):
    def __init__(self, lex):
        Token.__init__(self, lex, None)

    def transform_to(self, ttype):
        return Token(self.lex, ttype)

    @property
    def is_valid(self):
        return False
