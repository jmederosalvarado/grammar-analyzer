from pycmp.grammar import Grammar
from pycmp.parsing import ShiftReduceParser, SLR1Parser


def slr_table_analizer(G):
    parser = SLR1Parser(G)

    try:
        parser._build_parsing_table()
    except AssertionError:
        return None, "Shift-Reduce or Reduce-Reduce conflict!!!"  #To Do

    conflicts = []

    action = parser.action
    goto = parser.goproductions = {}
    productions = {}
    states = {}

    for p in G.productions:
        productions[p] = False

    for key in action:
        states[key[0]] = False

    for key, value in goto:
        states[value] = True

    for key, value in action:
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
