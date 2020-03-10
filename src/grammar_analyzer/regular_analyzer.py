from pycmp.grammar import Grammar
from pycmp.automata import NFA, DFA, nfa_to_dfa
from pycmp.regex import regex_tokenizer, Regex
from pycmp.regex import EpsilonNode, SymbolNode, ClosureNode, ConcatNode, UnionNode
from pycmp.evaluation import evaluate_parse
from pycmp.utils import pprint
from utils import visitor

__nosymbol = "@"
__epsilon = "ε"


def is_regular_grammar(grammar: Grammar):
    for nt, right in grammar.productions:
        if right.is_epsilon or len(right) == 0:
            if nt == grammar.start_symbol:
                continue
            return False
        if not right[0].is_terminal:
            return False
        if len(right) >= 2 and not right[1].is_nonterminal:
            return False
        if len(right) > 2:
            return False
    return True


def grammar_to_automaton(grammar):
    nonterminals = (nt for nt in grammar.nonterminals if nt != grammar.start_symbol)
    state_map = {nt: i + 1 for i, nt in enumerate(nonterminals)}
    state_map[grammar.start_symbol] = 0

    states = len(grammar.nonterminals) + 1
    final = states - 1
    transitions = {}

    for left, right in grammar.productions:
        origin = state_map[left]

        if right.is_epsilon or len(right) == 0:
            symbol = __epsilon
        else:
            symbol = right[0].name

        dest = state_map[right[1]] if len(right) == 2 else final
        try:
            if not dest in transitions[origin, symbol]:
                transitions[origin, symbol].append(dest)
        except KeyError:
            transitions[origin, symbol] = [dest]

    return NFA(states, {final}, transitions)


def automaton_to_regex(automaton):
    automaton = nfa_to_dfa(automaton)

    states, transitions = __automaton_to_gnfa(automaton)
    regex = __gnfa_to_regex(list(range(states)), transitions)
    ast = __get_regex_ast(regex)
    return __simplify_regex(ast)


def __get_regex_ast(regex):
    tokens = regex_tokenizer(regex, Regex.grammar)
    parse = Regex.parser([t.ttype for t in tokens])
    return evaluate_parse(parse, tokens)


@visitor.on("regex")
def __simplify_regex(regex):
    pass


@__simplify_regex.when(EpsilonNode)
def __simplify_regex_eps(regex: EpsilonNode):
    return regex.lex


@__simplify_regex.when(SymbolNode)
def __simplify_regex_symbol(regex: SymbolNode):
    return regex.lex


@__simplify_regex.when(UnionNode)
def __simplify_regex_union(regex: UnionNode):
    left = __simplify_regex(regex.left)
    right = __simplify_regex(regex.right)

    if left == __nosymbol:
        # print(f"{left} | {right} -> {right}")
        return right
    if right == __nosymbol:
        # print(f"{left} | {right} -> {left}")
        return left
    # print(f"{left} | {right} -> {left} | {right}")
    return f"({left}|{right})"


@__simplify_regex.when(ClosureNode)
def __simplify_regex_closure(regex: ClosureNode):
    operand = __simplify_regex(regex.node)
    if operand == __nosymbol:
        # print(f"{operand}* -> {__epsilon}")
        return __epsilon
    # print(f"{operand}* -> ({operand})*")
    return f"({operand})*"


@__simplify_regex.when(ConcatNode)
def __simplify_regex_concat(regex: ConcatNode):
    left = __simplify_regex(regex.left)
    right = __simplify_regex(regex.right)
    if left == __nosymbol or right == __nosymbol:
        # print(f"{left} {right} -> {__nosymbol}")
        return __nosymbol
    # print(f"{left} {right} -> ({left})({right})")
    return f"({left})({right})"


def __gnfa_to_regex(states, transitions):
    if len(states) == 2:
        return transitions[states[0], states[-1]]

    # remove state
    qrip = states.pop(1)
    for qi in states[:-1]:
        for qj in states[1:]:
            r1, r2, r3, r4 = (
                transitions[qi, qrip],
                transitions[qrip, qrip],
                transitions[qrip, qj],
                transitions[qi, qj],
            )
            transitions[qi, qj] = f"({r1})({r2})*({r3})|({r4})"

    return __gnfa_to_regex(states, transitions)


def __automaton_to_gnfa(automaton):
    states = automaton.states + 2
    start, old_start = 0, 1
    final = states - 1

    transitions = {}
    for origin in range(automaton.states):
        for dest in range(automaton.states):
            trans_syms = []

            for symbol in automaton.vocabulary:
                dests = automaton.transitions[origin].get(symbol)
                if dests is not None and dest in dests:
                    trans_syms.append(symbol)

            trans_regex = __nosymbol if not trans_syms else "|".join(trans_syms)
            transitions[old_start + origin, old_start + dest] = trans_regex

    ## Add transitions from start state ...

    for state in range(automaton.states):
        transitions[start, old_start + state] = __nosymbol
    transitions[start, old_start] = __epsilon
    transitions[start, final] = __nosymbol

    ## Add transitions to final state ...
    for state in range(automaton.states):
        symbol = __epsilon if state in automaton.finals else __nosymbol
        transitions[old_start + state, final] = symbol

    return states, transitions
