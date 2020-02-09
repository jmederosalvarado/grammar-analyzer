from pycmp.lexer import Lexer


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
