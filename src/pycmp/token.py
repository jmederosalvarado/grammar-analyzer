class Token:
    def __init__(self, lex, ttype):
        self.lex = lex
        self.ttype = ttype

    def __str__(self):
        return f"{self.ttype}: {self.lex}"

    def __repr__(self):
        return str(self)

    def __eq__(self, value):
        if type(self) != type(value):
            return False
        return self.lex == value.lex and self.ttype == value.ttype

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
