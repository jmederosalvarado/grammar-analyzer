from pycmp.lexer import Lexer


def build_input_lexer(grammar):
    digits = "|".join(str(n) for n in range(10))
    letters = "|".join(chr(n) for n in range(ord("a"), ord("z") + 1))
    others = "|".join([r"\(", r"\)"])
    symbols = f"{letters}|{digits}|{others}"
    lexer = Lexer(
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
    return lambda text: [t for t in lexer(text) if t.ttype is not None]
