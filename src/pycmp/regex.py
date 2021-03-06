from pycmp.grammar import Grammar
from pycmp.automata import NFA, DFA
from pycmp.automata import automata_closure, automata_union, automata_concatenation
from pycmp.automata import nfa_to_dfa, automata_minimization
from pycmp.ast import Node, AtomicNode, UnaryNode, BinaryNode
from pycmp.token import Token
from pycmp.parsing import build_ll_parser
from pycmp.evaluation import evaluate_parse


class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states=1, finals=[0], transitions={})


class SymbolNode(AtomicNode):
    def evaluate(self):
        transitions = {(0, self.lex): 1}
        return DFA(states=2, finals=[1], transitions=transitions)


class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)


class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)


def regex_tokenizer(text, grammar, skip_whitespaces=True, scape="\\"):
    tokens = []

    fixed_tokens = {"(", ")", "*", "|", "ε"}

    scape_next = False
    for char in text:
        if scape_next:
            tokens.append(Token(char, grammar["symbol"]))
            scape_next = False
            continue

        if char == scape:
            scape_next = True
            continue

        if skip_whitespaces and char.isspace():
            continue

        ttype = grammar[char] if char in fixed_tokens else grammar["symbol"]
        tokens.append(Token(char, ttype))

    tokens.append(Token("$", grammar.eof))
    return tokens


def build_regex_grammar():
    G = Grammar()

    E = G.add_nonterminal("E", True)
    T, F, A, X, Y, Z = G.add_nonterminals("T F A X Y Z")
    pipe, star, opar, cpar, symbol, epsilon = G.add_terminals("| * ( ) symbol ε")

    E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]

    X %= pipe + T + X, lambda h, s: s[3], None, None, lambda h, s: UnionNode(h[0], s[2])
    X %= G.epsilon, lambda h, s: h[0]

    T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]

    Y %= F + Y, lambda h, s: s[2], None, lambda h, s: ConcatNode(h[0], s[1])
    Y %= G.epsilon, lambda h, s: h[0]

    F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]

    Z %= star + Z, lambda h, s: s[2], None, lambda h, s: ClosureNode(h[0])
    Z %= G.epsilon, lambda h, s: h[0]

    A %= symbol, lambda h, s: SymbolNode(s[1])
    A %= opar + E + cpar, lambda h, s: s[2], None, None, None
    A %= epsilon, lambda h, s: EpsilonNode(s[1])

    return G


class Regex:
    grammar = build_regex_grammar()
    parser = build_ll_parser(grammar)

    def __init__(self, regex, skip_whitespaces=False):
        self.regex = regex
        self.automaton = Regex.build_automaton(regex, skip_whitespaces=skip_whitespaces)

    def __call__(self, text):
        return self.automaton.recognize(text)

    @classmethod
    def build_automaton(cls, regex, skip_whitespaces=False):
        tokens = regex_tokenizer(regex, cls.grammar, skip_whitespaces=skip_whitespaces)
        parse = cls.parser([t.ttype for t in tokens])
        ast = evaluate_parse(parse, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        minimized = automata_minimization(dfa)

        return minimized
