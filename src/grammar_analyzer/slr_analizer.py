from pycmp.grammar import Grammar
from pycmp.parsing import ShiftReduceParser, SLR1Parser


class _SLR1Parser(SLR1Parser):
    @staticmethod
    def _register(table, key, value):
        if key not in table:
            table[key] = []
        if not value in table[key]:
            table[key].append(value)


def slr_table_analizer(G):
    parser = _SLR1Parser(G)
    parser._build_parsing_table()

    conflicts = []

    action = parser.action
    goto = parser.goproductions = {}
    productions = {}
    states = {}

    for p in G.productions:
        productions[p] = False

    for key in action:
        states[key[0]] = False

    for key, values in goto:
        if len(value) > 1:
            conflicts.append(key, "Shift-Reduce or Reduce-Reduce conflict!!!")
        for value in values:
            states[value] = True

    for key, values in action:
        if len(value) > 1:
            conflicts.append(key, "Shift-Reduce or Reduce-Reduce conflict!!!")

        for value in values:

            if value[0] == parser.REDUCE:
                productions[value[1]] = True

            if value[0] == parser.SHIFT:
                states[value[1]] = True

    for key, value in states:
        if not value:
            conflicts.append((key, "state never reached"))

    for key, value in productions:
        if not value:
            conflicts.append((key, "production never reached"))

    return conflicts


class DerivationTreeNode(object):
    def init(self, value, children=None):
        self.value = value
        self.children = children or []


def build_derivation_tree(right_parse, i=-1):
    if i == -1:
        i = len(right_parse - 1)

    production = right_parse[i]
    node = DerivationTreeNode(production.Left)

    sentence = production.right
    for s in range(sentence, 0, -1):
        if sentence[s].IsTerminal or sentence[s].IsEpsilon:
            node.children.append(DerivationTreeNode(sentence[s]))
        else:
            i, child = build_derivation_tree(right_parse, i - 1)
            node.children.append(child)
    return i, node
