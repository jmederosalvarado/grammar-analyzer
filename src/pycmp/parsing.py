from itertools import islice
from pycmp.utils import ContainerSet
from pycmp.automata import State, multiline_formatter
from pycmp.grammar import Item


def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    # alpha = X1 ... XN
    # First(Xi) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ?
    #     First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ?
    #     epsilon pertence a First(X) y al First(alpha)
    for s in alpha:
        first_alpha.update(firsts[s])
        if not firsts[s].contains_epsilon:
            break
    else:
        first_alpha.set_epsilon()

    return first_alpha


def compute_firsts(grammar):
    firsts = {}
    change = True

    # init First(Vt)
    for terminal in grammar.terminals:
        firsts[terminal] = ContainerSet(terminal)

    # init First(Vn)
    for nonterminal in grammar.nonterminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False

        # P: X -> alpha
        for production in grammar.productions:
            X = production.left
            alpha = production.right

            # get current First(X)
            first_X = firsts[X]

            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except:
                first_alpha = firsts[alpha] = ContainerSet()

            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)

            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    # First(Vt) + First(Vt) + First(RightSides)
    return firsts


def compute_follows(g, firsts):
    follows = {}
    change = True

    local_firsts = {}

    # init Follow(Vn)
    for nonterminal in g.nonterminals:
        follows[nonterminal] = ContainerSet()
    follows[g.start_symbol] = ContainerSet(g.eof)

    while change:
        change = False

        # P: X -> alpha
        for production in g.productions:
            x = production.left
            alpha = production.right

            follow_x = follows[x]

            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            for i, y in enumerate(alpha):
                if y not in g.nonterminals:
                    continue
                beta = alpha[i+1:]
                if beta:
                    if beta not in local_firsts:
                        local_firsts[beta] = compute_local_first(firsts, beta)
                    change |= follows[y].update(local_firsts[beta])
                if not beta or local_firsts[beta].contains_epsilon:
                    change |= follows[y].update(follow_x)

    # Follow(Vn)
    return follows


def build_ll_table(g, firsts, follows):
    # init parsing table
    table = {}

    # P: X -> alpha
    for production in g.productions:
        x = production.left
        alpha = production.right

        # working with symbols on First(alpha)
        for t in firsts[alpha]:
            try:
                table[x, t].append(production)
            except KeyError:
                table[x, t] = [production]

        # working with epsilon
        if firsts[alpha].contains_epsilon:
            for t in g.terminals + [g.eof]:
                if t in follows[x]:
                    try:
                        table[x, t].append(production)
                    except KeyError:
                        table[x, t] = [production]

    return table


def build_ll_parser(grammar, table=None, firsts=None, follows=None):
    # checking table
    if table is None:
        if firsts is None:
            firsts = compute_firsts(grammar)
        if follows is None:
            follows = compute_follows(grammar, firsts)
        table = build_ll_table(grammar, firsts, follows)

    def parser(tokens):
        stack = [grammar.start_symbol]
        cursor = 0
        output = []

        # parsing tokens
        while len(stack) > 0:
            top = stack.pop()
            a = tokens[cursor]

            if top.is_terminal and tokens[cursor] == top:
                cursor += 1

            else:
                try:
                    production = table[(top, a)]
                except KeyError:
                    raise Exception('Parsing error')

                if len(production) > 1:
                    raise Exception('Parsing error')

                production = production[0]
                output.append(production)
                stack.extend(reversed(production.right))

        return output

    return lambda tokens: parser([t.ttype for t in tokens])


class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, grammar, verbose=False):
        self.grammar = grammar
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []

        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose:
                print(stack, '<---||--->', w[cursor:])

            try:
                action, tag = self.action[state, lookahead]
            except KeyError:
                raise Exception('Parsing error')

            assert action in [self.SHIFT, self.REDUCE, self.OK], 'You screwed up'

            # Shift case
            if action == self.SHIFT:
                stack.append(tag)
                cursor += 1

            # Reduce case
            if action == self.REDUCE:
                output.append(tag)
                stack = stack[:-len(tag.Right)]
                stack.append(self.goto[stack[-1], tag.Left])

            # OK case
            if action == self.OK:
                break

        return output


def build_lr0_automaton(grammar):
    assert len(grammar.start_symbol.productions) == 1, 'Grammar must be augmented'

    start_production = grammar.start_symbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [start_item]
    visited = {start_item: automaton}

    while pending:
        current_item = pending.pop()
        if current_item.is_reduce_item:
            continue

        next_symbol = current_item.next_symbol
        next_item = current_item.next_item()

        transitions = [(next_symbol.name, next_item)]
        if next_symbol.is_nonterminal:
            transitions.extend([(None, Item(prod, 0)) for prod in next_symbol.productions])

        current_state = visited[current_item]

        for next_symbol, next_item in transitions:
            try:
                next_state = visited[next_item]
            except KeyError:
                pending.append(next_item)
                next_state = State(next_item, True)
                visited[next_item] = next_state
            if next_symbol:
                current_state.add_transition(next_symbol, next_state)
            else:
                current_state.add_epsilon_transition(next_state)

    return automaton


class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        grammar = self.grammar.AugmentedGrammar(True)
        firsts = compute_firsts(grammar)
        follows = compute_follows(grammar, firsts)

        automaton = build_lr0_automaton(grammar).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state

                if item.IsReduceItem:
                    action = self.REDUCE if item.production.Left != grammar.start_symbol else self.OK
                    for c in follows[item.production.Left]:
                        self._register(self.action, (idx, c), (action, item.production))
                    continue

                x = item.NextSymbol
                try:
                    dest = node.transitions[x.Name][0]
                except KeyError:
                    continue
                if x.IsTerminal:
                    self._register(self.action, (idx, x), (self.SHIFT, dest.idx))
                else:
                    self._register(self.goto, (idx, x), dest.idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value


def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    # Compute lookahead for child items
    for preview in item.Preview():
        preview_firsts = compute_local_first(firsts, preview)
        lookaheads.update(preview_firsts)

    assert not lookaheads.contains_epsilon
    # Build and return child items
    return [Item(prod, 0, lookaheads) for prod in next_symbol.productions]


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}


def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


def build_lr1_automaton(G):
    assert len(G.start_symbol.productions) == 1, 'Grammar must be augmented'

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.start_symbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            # Get/Build `next_state`
            next_ = frozenset(goto_lr1(closure_lr1(current, firsts), symbol, just_kernel=True))
            if not next_:
                continue

            try:
                next_state = visited[next_]
            except KeyError:
                pending.append(next_)
                next_closure = frozenset(closure_lr1(next_, firsts))
                next_state = visited[next_] = State(next_closure, True)

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        grammar = self.grammar.AugmentedGrammar(True)

        automaton = build_lr1_automaton(grammar)
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    is_start = item.production.Left == grammar.start_symbol
                    for s in item.lookaheads:
                        action = self.OK if is_start and s == grammar.EOF else self.REDUCE
                        self._register(self.action, (idx, s), (action, item.production))
                    continue

                x = item.NextSymbol
                try:
                    dest = node.transitions[x.Name][0]
                except KeyError:
                    continue
                if x.IsTerminal:
                    self._register(self.action, (idx, x), (self.SHIFT, dest.idx))
                else:
                    self._register(self.goto, (idx, x), dest.idx)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
