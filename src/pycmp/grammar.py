import json


class Symbol(object):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(self, other)

        raise TypeError(other)

    def __or__(self, other):
        if isinstance(other, (Sentence)):
            return SentenceList(Sentence(self), other)

        raise TypeError(other)

    @property
    def is_epsilon(self):
        return False

    def __len__(self):
        return 1


class NonTerminal(Symbol):
    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.productions = []

    def __imod__(self, other):
        if isinstance(other, (Sentence)):
            p = Production(self, other)
            self.grammar.add_production(p)
            return self

        if isinstance(other, tuple):
            assert len(other) > 1

            if len(other) == 2:
                other += (None,) * len(other[0])

            assert (
                len(other) == len(other[0]) + 2
            ), "Debe definirse una, y solo una, regla por cada sé“†mbolo de la producciè´¸n"

            if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
                p = AttributedProduction(self, other[0], other[1:])
            else:
                raise Exception("")

            self.grammar.add_production(p)
            return self

        if isinstance(other, Symbol):
            p = Production(self, Sentence(other))
            self.grammar.add_production(p)
            return self

        if isinstance(other, SentenceList):
            for s in other:
                p = Production(self, s)
                self.grammar.add_production(p)

            return self

        raise TypeError(other)

    @property
    def is_terminal(self):
        return False

    @property
    def is_nonterminal(self):
        return True

    @property
    def is_epsilon(self):
        return False


class Terminal(Symbol):
    def __init__(self, name, grammar):
        super().__init__(name, grammar)

    @property
    def is_terminal(self):
        return True

    @property
    def is_nonterminal(self):
        return False

    @property
    def is_epsilon(self):
        return False


class EOF(Terminal):
    def __init__(self, Grammar):
        super().__init__("$", Grammar)


class Sentence(object):
    def __init__(self, *args):
        self._symbols = tuple(x for x in args if not x.is_epsilon)
        self.hash = hash(self._symbols)

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(*(self._symbols + (other,)))

        if isinstance(other, Sentence):
            return Sentence(*(self._symbols + other._symbols))

        raise TypeError(other)

    def __or__(self, other):
        if isinstance(other, Sentence):
            return SentenceList(self, other)

        if isinstance(other, Symbol):
            return SentenceList(self, Sentence(other))

        raise TypeError(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ("%s " * len(self._symbols) % tuple(self._symbols)).strip()

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    def __eq__(self, other):
        return self._symbols == other._symbols

    def __hash__(self):
        return self.hash

    @property
    def is_epsilon(self):
        return False


class SentenceList(object):
    def __init__(self, *args):
        self._sentences = list(args)

    def add(self, symbol):
        if not symbol and (symbol is None or not symbol.is_epsilon):
            raise ValueError(symbol)

        self._sentences.append(symbol)

    def __iter__(self):
        return iter(self._sentences)

    def __or__(self, other):
        if isinstance(other, Sentence):
            self.add(other)
            return self

        if isinstance(other, Symbol):
            return self | Sentence(other)


class Epsilon(Terminal, Sentence):
    def __init__(self, grammar):
        super().__init__("epsilon", grammar)

    def __str__(self):
        return "e"

    def __repr__(self):
        return "epsilon"

    def __iter__(self):
        yield from ()

    def __len__(self):
        return 0

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    @property
    def is_epsilon(self):
        return True


class Production(object):
    def __init__(self, nonterminal, sentence):
        self.left = nonterminal
        self.right = sentence

    def __str__(self):
        return "%s := %s" % (self.left, self.right)

    def __repr__(self):
        return "%s -> %s" % (self.left, self.right)

    def __iter__(self):
        yield self.left
        yield self.right

    def __eq__(self, other):
        return (
            isinstance(other, Production)
            and self.left == other.left
            and self.right == other.right
        )

    def __hash__(self):
        return hash((self.left, self.right))

    @property
    def is_epsilon(self):
        return self.right.is_epsilon


class AttributedProduction(Production):
    def __init__(self, nonterminal, sentence, attributes):
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super().__init__(nonterminal, sentence)

        self.attributes = attributes

    def __str__(self):
        return "%s := %s" % (self.left, self.right)

    def __repr__(self):
        return "%s -> %s" % (self.left, self.right)

    def __iter__(self):
        yield self.left
        yield self.right

    @property
    def is_epsilon(self):
        return self.right.is_epsilon

    def synthesize(self):
        pass


class Grammar:
    def __init__(self):
        self.productions = []
        self.nonterminals = []
        self.terminals = []
        self.start_symbol = None
        self.ptype = None
        self.epsilon = Epsilon(self)
        self.eof = EOF(self)

        self.symbol_dict = {"$": self.eof}

    def add_nonterminal(self, name, start_symbol=False):
        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = NonTerminal(name, self)

        if start_symbol:
            if self.start_symbol is None:
                self.start_symbol = term
            else:
                raise Exception("Cannot define more than one start symbol.")

        self.nonterminals.append(term)
        self.symbol_dict[name] = term
        return term

    def add_nonterminals(self, names):
        ans = tuple((self.add_nonterminal(x) for x in names.strip().split()))
        return ans

    def add_production(self, production):
        if len(self.productions) == 0:
            self.ptype = type(production)

        assert type(production) == self.ptype, "The Productions most be of only 1 type."

        production.left.productions.append(production)
        self.productions.append(production)

    def add_terminal(self, name):
        name = name.strip()
        if not name:
            raise Exception("Empty name")

        term = Terminal(name, self)
        self.terminals.append(term)
        self.symbol_dict[name] = term
        return term

    def add_terminals(self, names):
        ans = tuple((self.add_terminal(x) for x in names.strip().split()))
        return ans

    def __str__(self):
        mul = "%s, "

        ans = "Non-Terminals:\n\t"

        nonterminals = mul * (len(self.nonterminals) - 1) + "%s\n"

        ans += nonterminals % tuple(self.nonterminals)

        ans += "Terminals:\n\t"

        terminals = mul * (len(self.terminals) - 1) + "%s\n"

        ans += terminals % tuple(self.terminals)

        ans += "Productions:\n\t"

        ans += str(self.productions)

        return ans

    def __getitem__(self, name):
        try:
            return self.symbol_dict[name]
        except KeyError:
            return None

    @property
    def to_json(self):
        productions = []

        for p in self.productions:
            head = p.left.name

            body = []

            for s in p.right:
                body.append(s.name)

            productions.append({"head": head, "body": body})

        d = {
            "start_symbol": self.start_symbol.name,
            "nonterminals": [symb.name for symb in self.nonterminals],
            "terminals": [symb.name for symb in self.terminals],
            "productions": productions,
        }

        return json.dumps(d)

    @staticmethod
    def from_json(data):
        data = json.loads(data)

        g = Grammar()
        dic = {"epsilon": g.epsilon}

        for term in data["terminals"]:
            dic[term] = g.add_terminal(term)

        for nonterm in data["nonterminals"]:
            dic[nonterm] = g.add_nonterminal(nonterm)

        for p in data["productions"]:
            head = p["head"]
            dic[head] %= Sentence(*[dic[term] for term in p["body"]])

        start_symbol = data["start_symbol"]
        g.start_symbol = dic[start_symbol]

        g.ptype = Production

        return g

    def copy(self):
        g = Grammar()
        g.productions = self.productions.copy()
        g.nonterminals = self.nonterminals.copy()
        g.terminals = self.terminals.copy()
        g.ptype = self.ptype
        g.start_symbol = self.start_symbol
        g.epsilon = self.epsilon
        g.eof = self.eof
        g.symbol_dict = self.symbol_dict.copy()

        return g

    @property
    def is_augmented_grammar(self):
        augmented = 0
        for left, _ in self.productions:
            if self.start_symbol == left:
                augmented += 1
        if augmented <= 1:
            return True
        else:
            return False

    def get_augmented_grammar(self, force=False):
        if not self.is_augmented_grammar or force:
            g = self.copy()
            s = g.start_symbol
            g.start_symbol = None
            ss = g.add_nonterminal("s'", True)
            if g.ptype is AttributedProduction:
                ss %= s + g.epsilon, lambda x: x
            else:
                ss %= s + g.epsilon

            return g
        else:
            return self.copy()


class Item:
    def __init__(self, production, pos, lookaheads=[]):
        self.production = production
        self.pos = pos
        self.lookaheads = frozenset(look for look in lookaheads)

    def __str__(self):
        s = str(self.production.left) + " -> "
        if len(self.production.right) > 0:
            for i, _ in enumerate(self.production.right):
                if i == self.pos:
                    s += "."
                s += str(self.production.right[i])
            if self.pos == len(self.production.right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.lookaheads)[10:-1]
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            (self.pos == other.pos)
            and (self.production == other.production)
            and (set(self.lookaheads) == set(other.lookaheads))
        )

    def __hash__(self):
        return hash((self.production, self.pos, self.lookaheads))

    @property
    def is_reduce_item(self):
        return len(self.production.right) == self.pos

    @property
    def next_symbol(self):
        if self.pos < len(self.production.right):
            return self.production.right[self.pos]
        else:
            return None

    def next_item(self):
        if self.pos < len(self.production.right):
            return Item(self.production, self.pos + 1, self.lookaheads)
        else:
            return None

    def preview(self, skip=1):
        unseen = self.production.right[self.pos + skip :]
        return [unseen + (lookahead,) for lookahead in self.lookaheads]

    def center(self):
        return Item(self.production, self.pos)
