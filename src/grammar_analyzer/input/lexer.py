from pycmp.lexer import Lexer
from grammar_analyzer.input.grammar import input_grammar


def build_input_lexer():
    digits = "|".join(str(n) for n in range(10))
    letters = "|".join(chr(n) for n in range(ord("a"), ord("z") + 1))
    others = "|".join([r"\(", r"\)"])
    symbols = f"{letters}|{digits}|{others}"
    lexer = Lexer(
        [
            (input_grammar["eps"], "eps"),
            (input_grammar["|"], r"\|"),
            (input_grammar["->"], "->"),
            (input_grammar["eol"], "\\n"),
            (None, "  *"),
            (input_grammar["symbol"], f"({symbols})({symbols})*"),
        ],
        input_grammar.eof,
    )
    return lambda text: [t for t in lexer(text) if t.ttype is not None]
