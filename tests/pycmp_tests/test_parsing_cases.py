from pycmp.grammar import Grammar, Sentence, Production, AttributedProduction
from pycmp.utils import ContainerSet
from pycmp.token import Token

test_compute_firsts_cases = []
test_compute_follows_cases = []
test_build_ll_table_cases = []
test_build_ll_parser_cases = []
test_evaluate_parse_cases = []

grammar = Grammar()
E = grammar.add_nonterminal('E', True)
T, F, X, Y = grammar.add_nonterminals('T F X Y')
plus, minus, star, div, opar, cpar, num = grammar.add_terminals('+ - * / ( ) num')

E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]

X %= plus + T + X, lambda h, s: s[3], None, None, lambda h, s: h[0] + s[2]
X %= minus + T + X, lambda h, s: s[3], None, None, lambda h, s: h[0] - s[2]
X %= grammar.epsilon, lambda h, s: h[0]

T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]

Y %= star + F + Y, lambda h, s: s[3], None, None, lambda h, s: h[0] * s[2]
Y %= div + F + Y, lambda h, s: s[3], None, None, lambda h, s: h[0] / s[2]
Y %= grammar.epsilon, lambda h, s: h[0]

F %= opar + E + cpar, lambda h, s: s[2], None, None, None
F %= num, lambda h, s: float(s[1]), None

firsts = {
    grammar['+']: ContainerSet(grammar['+'], contains_epsilon=False),
    grammar['-']: ContainerSet(grammar['-'], contains_epsilon=False),
    grammar['*']: ContainerSet(grammar['*'], contains_epsilon=False),
    grammar['/']: ContainerSet(grammar['/'], contains_epsilon=False),
    grammar['(']: ContainerSet(grammar['('], contains_epsilon=False),
    grammar[')']: ContainerSet(grammar[')'], contains_epsilon=False),
    grammar['num']: ContainerSet(grammar['num'], contains_epsilon=False),
    grammar['E']: ContainerSet(grammar['num'], grammar['('], contains_epsilon=False),
    grammar['T']: ContainerSet(grammar['num'], grammar['('], contains_epsilon=False),
    grammar['F']: ContainerSet(grammar['num'], grammar['('], contains_epsilon=False),
    grammar['X']: ContainerSet(grammar['-'], grammar['+'], contains_epsilon=True),
    grammar['Y']: ContainerSet(grammar['/'], grammar['*'], contains_epsilon=True),
    Sentence(grammar['T'], grammar['X']): ContainerSet(grammar['num'], grammar['('], contains_epsilon=False),
    Sentence(grammar['+'], grammar['T'], grammar['X']): ContainerSet(grammar['+'], contains_epsilon=False),
    Sentence(grammar['-'], grammar['T'], grammar['X']): ContainerSet(grammar['-'], contains_epsilon=False),
    grammar.epsilon: ContainerSet(contains_epsilon=True),
    Sentence(grammar['F'], grammar['Y']): ContainerSet(grammar['num'], grammar['('], contains_epsilon=False),
    Sentence(grammar['*'], grammar['F'], grammar['Y']): ContainerSet(grammar['*'], contains_epsilon=False),
    Sentence(grammar['/'], grammar['F'], grammar['Y']): ContainerSet(grammar['/'], contains_epsilon=False),
    Sentence(grammar['num']): ContainerSet(grammar['num'], contains_epsilon=False),
    Sentence(grammar['('], grammar['E'], grammar[')']): ContainerSet(grammar['('], contains_epsilon=False)
}
test_compute_firsts_cases.append((grammar, firsts))

follows = {
    grammar['E']: ContainerSet(grammar[')'], grammar.eof, contains_epsilon=False),
    grammar['T']: ContainerSet(grammar[')'], grammar['-'], grammar.eof, grammar['+'], contains_epsilon=False),
    grammar['F']: ContainerSet(grammar['-'], grammar.eof, grammar['*'], grammar['/'], grammar[')'], grammar['+'], contains_epsilon=False),
    grammar['X']: ContainerSet(grammar[')'], grammar.eof, contains_epsilon=False),
    grammar['Y']: ContainerSet(grammar[')'], grammar['-'], grammar.eof, grammar['+'], contains_epsilon=False)
}
test_compute_follows_cases.append((grammar, firsts, follows))

table = {
    (grammar['E'], grammar['num']): [Production(grammar['E'], Sentence(grammar['T'], grammar['X']))],
    (grammar['E'], grammar['(']): [Production(grammar['E'], Sentence(grammar['T'], grammar['X']))],
    (grammar['X'], grammar['+']): [Production(grammar['X'], Sentence(grammar['+'], grammar['T'], grammar['X']))],
    (grammar['X'], grammar['-']): [Production(grammar['X'], Sentence(grammar['-'], grammar['T'], grammar['X']))],
    (grammar['X'], grammar[')']): [Production(grammar['X'], grammar.epsilon)],
    (grammar['X'], grammar.eof): [Production(grammar['X'], grammar.epsilon)],
    (grammar['T'], grammar['num']): [Production(grammar['T'], Sentence(grammar['F'], grammar['Y']))],
    (grammar['T'], grammar['(']): [Production(grammar['T'], Sentence(grammar['F'], grammar['Y']))],
    (grammar['Y'], grammar['*']): [Production(grammar['Y'], Sentence(grammar['*'], grammar['F'], grammar['Y']))],
    (grammar['Y'], grammar['/']): [Production(grammar['Y'], Sentence(grammar['/'], grammar['F'], grammar['Y']))],
    (grammar['Y'], grammar[')']): [Production(grammar['Y'], grammar.epsilon)],
    (grammar['Y'], grammar['-']): [Production(grammar['Y'], grammar.epsilon)],
    (grammar['Y'], grammar.eof): [Production(grammar['Y'], grammar.epsilon)],
    (grammar['Y'], grammar['+']): [Production(grammar['Y'], grammar.epsilon)],
    (grammar['F'], grammar['num']): [Production(grammar['F'], Sentence(grammar['num']))],
    (grammar['F'], grammar['(']): [Production(grammar['F'], Sentence(grammar['('], grammar['E'], grammar[')']))]
}
test_build_ll_table_cases.append((grammar, firsts, follows, table))

tokens = [
    Token('1', num),
    Token('*', star),
    Token('1', num),
    Token('*', star),
    Token('1', num),
    Token('+', plus),
    Token('1', num),
    Token('*', star),
    Token('1', num),
    Token('+', plus),
    Token('1', num),
    Token('+', plus),
    Token('1', num),
    Token('$', grammar.eof)
]
test_build_ll_parser_cases.append((
    grammar, firsts, follows, table, tokens, [
        Production(E, Sentence(T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, Sentence(star, F, Y)),
        Production(F, Sentence(num)),
        Production(Y, Sentence(star, F, Y)),
        Production(F, Sentence(num)),
        Production(Y, grammar.epsilon),
        Production(X, Sentence(plus, T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, Sentence(star, F, Y)),
        Production(F, Sentence(num)),
        Production(Y, grammar.epsilon),
        Production(X, Sentence(plus, T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, grammar.epsilon),
        Production(X, Sentence(plus, T, X)),
        Production(T, Sentence(F, Y)),
        Production(F, Sentence(num)),
        Production(Y, grammar.epsilon),
        Production(X, grammar.epsilon),
    ]
))

grammar = Grammar()
S = grammar.add_nonterminal('S', True)
A, B = grammar.add_nonterminals('A B')
a, b = grammar.add_terminals('a b')

S %= A + B
A %= a + A | a
B %= b + B | b

firsts = {
    a: ContainerSet(a, contains_epsilon=False),
    b: ContainerSet(b, contains_epsilon=False),
    S: ContainerSet(a, contains_epsilon=False),
    A: ContainerSet(a, contains_epsilon=False),
    B: ContainerSet(b, contains_epsilon=False),
    Sentence(A, B): ContainerSet(a, contains_epsilon=False),
    Sentence(a, A): ContainerSet(a, contains_epsilon=False),
    Sentence(a): ContainerSet(a, contains_epsilon=False),
    Sentence(b, B): ContainerSet(b, contains_epsilon=False),
    Sentence(b): ContainerSet(b, contains_epsilon=False)
}
test_compute_firsts_cases.append((grammar, firsts))

follows = {
    S: ContainerSet(grammar.eof, contains_epsilon=False),
    A: ContainerSet(b, contains_epsilon=False),
    B: ContainerSet(grammar.eof, contains_epsilon=False)
}
test_compute_follows_cases.append((grammar, firsts, follows))

table = {
    (S, a): [Production(S, Sentence(A, B))],
    (A, a): [Production(A, Sentence(a, A)), Production(A, Sentence(a))],
    (B, b): [Production(B, Sentence(b, B)), Production(B, Sentence(b))]
}
test_build_ll_table_cases.append((grammar, firsts, follows, table))

grammar = Grammar()
S = grammar.add_nonterminal('S', True)
A, B, C = grammar.add_nonterminals('A B C')
a, b, c, d, f = grammar.add_terminals('a b c d f')

S %= a + A | B + C | f + B + f
A %= a + A | grammar.epsilon
B %= b + B | grammar.epsilon
C %= c + C | d

firsts = {
    a: ContainerSet(a, contains_epsilon=False),
    b: ContainerSet(b, contains_epsilon=False),
    c: ContainerSet(c, contains_epsilon=False),
    d: ContainerSet(d, contains_epsilon=False),
    f: ContainerSet(f, contains_epsilon=False),
    S: ContainerSet(d, a, f, c, b, contains_epsilon=False),
    A: ContainerSet(a, contains_epsilon=True),
    B: ContainerSet(b, contains_epsilon=True),
    C: ContainerSet(c, d, contains_epsilon=False),
    Sentence(a, A): ContainerSet(a, contains_epsilon=False),
    Sentence(B, C): ContainerSet(d, c, b, contains_epsilon=False),
    Sentence(f, B, f): ContainerSet(f, contains_epsilon=False),
    grammar.epsilon: ContainerSet(contains_epsilon=True),
    Sentence(b, B): ContainerSet(b, contains_epsilon=False),
    Sentence(c, C): ContainerSet(c, contains_epsilon=False),
    Sentence(d): ContainerSet(d, contains_epsilon=False)
}
test_compute_firsts_cases.append((grammar, firsts))

follows = {
    S: ContainerSet(grammar.eof, contains_epsilon=False),
    A: ContainerSet(grammar.eof, contains_epsilon=False),
    B: ContainerSet(d, f, c, contains_epsilon=False),
    C: ContainerSet(grammar.eof, contains_epsilon=False)
}
test_compute_follows_cases.append((grammar, firsts, follows))

table = {
    (S, a): [Production(S, Sentence(a, A))],
    (S, c): [Production(S, Sentence(B, C))],
    (S, b): [Production(S, Sentence(B, C))],
    (S, d): [Production(S, Sentence(B, C))],
    (S, f): [Production(S, Sentence(f, B, f))],
    (A, a): [Production(A, Sentence(a, A))],
    (A, grammar.eof): [Production(A, grammar.epsilon)],
    (B, b): [Production(B, Sentence(b, B))],
    (B, c): [Production(B, grammar.epsilon)],
    (B, f): [Production(B, grammar.epsilon)],
    (B, d): [Production(B, grammar.epsilon)],
    (C, c): [Production(C, Sentence(c, C))],
    (C, d): [Production(C, Sentence(d))]
}
test_build_ll_table_cases.append((grammar, firsts, follows, table))

tokens = [Token('b', b), Token('b', b), Token('d', d), Token('$', grammar.eof)]
test_build_ll_parser_cases.append((
    grammar, firsts, follows, table, tokens, [
        Production(S, Sentence(B, C)),
        Production(B, Sentence(b, B)),
        Production(B, Sentence(b, B)),
        Production(B, grammar.epsilon),
        Production(C, Sentence(d))
    ]
))


grammar = Grammar()
E = grammar.add_nonterminal('E', True)
T, F, X, Y = grammar.add_nonterminals('T F X Y')
plus, minus, star, div, opar, cpar, num = grammar.add_terminals('+ - * / ( ) num')

left_parse = [
    AttributedProduction(E, Sentence(T, X), [lambda h, s: s[2], None, lambda h, s: s[1]]),
    AttributedProduction(T, Sentence(F, Y), [lambda h, s: s[2], None, lambda h, s: s[1]]),
    AttributedProduction(F, Sentence(num), [lambda h, s: float(s[1]), None]),
    AttributedProduction(Y, grammar.epsilon, [lambda h, s: h[0]]),
    AttributedProduction(X, Sentence(plus, T, X), [lambda h, s: s[3], None, None, lambda h, s: h[0] + s[2]]),
    AttributedProduction(T, Sentence(F, Y), [lambda h, s: s[2], None, lambda h, s: s[1]]),
    AttributedProduction(F, Sentence(num), [lambda h, s: float(s[1]), None]),
    AttributedProduction(Y, grammar.epsilon, [lambda h, s: h[0]]),
    AttributedProduction(X, grammar.epsilon, [lambda h, s: h[0]]),
]
tokens = [
    Token('5.9', num),
    Token('+', plus),
    Token('4', num),
    Token('$', grammar.eof)
]

test_evaluate_parse_cases.append((left_parse, tokens, 9.9))

grammar = Grammar()
E = grammar.add_nonterminal('E', True)
T, F = grammar.add_nonterminals('T F')
plus, minus, star, div, opar, cpar, num = grammar.add_terminals('+ - * / ( ) int')

E %= E + plus + T | T  # | E + minus + T
T %= T + star + F | F  # | T + div + F
F %= num | opar + E + cpar

grammar = grammar.get_augmented_grammar()

test_build_lr0_automata_cases = [
    (grammar, 'E', True),
    (grammar, 'T*F', True),
    (grammar, ['E', '+', 'int'], True),
    (grammar, 'E*F', False),
]
