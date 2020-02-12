from pycmp.token import Token
from pycmp.regex import Regex
from pycmp.automata import State


class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()

    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            automaton = Regex.build_automaton(regex)
            automaton = State.from_nfa(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (n, token_type)
            regexs.append(automaton)

        return regexs

    def _build_automaton(self):
        start = State("start")
        for state in self.regexs:
            start.add_epsilon_transition(state)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ""

        for symbol in string:
            if not state.has_transition(symbol):
                break
            state = state[symbol][0]
            lex += symbol
            if state.final:
                final = state
                final_lex = lex

        return final, final_lex

    def _tokenize(self, text):
        i = 0
        while True:
            state, lex = self._walk(text[i:])
            if not state:
                break
            i += len(lex)
            highest = min([s for s in state.state if s.tag], key=lambda s: s.tag[0])
            yield lex, highest.tag[1]

        yield "$", self.eof

    def __call__(self, text):
        return [Token(lex, ttype) for lex, ttype in self._tokenize(text)]
