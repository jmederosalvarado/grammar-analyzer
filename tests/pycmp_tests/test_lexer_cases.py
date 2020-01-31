test_lexer_lex_cases = []
test_lexer_ttype_cases = []

nonzero_digits = '|'.join(str(n) for n in range(1, 10))
letters = '|'.join(chr(n) for n in range(ord('a'), ord('z')+1))
regexs = [
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    ('for', 'for'),
    ('foreach', 'foreach'),
    ('space', '  *'),
    ('id', f'({letters})({letters}|0|{nonzero_digits})*')
]

text = '5465 for 45foreach fore'
lexs, ttypes = zip(*[
    ('5465', 'num'),
    (' ', 'space'),
    ('for', 'for'),
    (' ', 'space'),
    ('45', 'num'),
    ('foreach', 'foreach'),
    (' ', 'space'),
    ('fore', 'id'),
    ('$', 'eof')
])
test_lexer_lex_cases.append((regexs, 'eof', text, lexs))
test_lexer_ttype_cases.append((regexs, 'eof', text, ttypes))

text = '4forense forforeach for4foreach foreach 4for'
lexs, ttypes = zip(*[
    ('4', 'num'),
    ('forense', 'id'),
    (' ', 'space'),
    ('forforeach', 'id'),
    (' ', 'space'),
    ('for4foreach', 'id'),
    (' ', 'space'),
    ('foreach', 'foreach'),
    (' ', 'space'),
    ('4', 'num'),
    ('for', 'for'),
    ('$', 'eof')
])
test_lexer_lex_cases.append((regexs, 'eof', text, lexs))
test_lexer_ttype_cases.append((regexs, 'eof', text, ttypes))
