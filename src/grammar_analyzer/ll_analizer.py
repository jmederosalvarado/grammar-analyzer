from pycmp.grammar import Grammar
from pycmp.parsing import compute_firsts, compute_follows, build_ll_table, build_ll_parser


# Returns bool : True if the grammar is LL(1), False otherwise
#         list of conflicts if exists
#         dictionary: parsing table
def table_analize(G):
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)

    table = build_ll_table(G, firsts, follows)

    conflicts = []

    for key, value in table.items():
        if len(value) > 1:
            conflicts.append((key, value))

    if len(conflicts) > 0:
        return True, conflicts, table

    return False, conflicts, table


def report_conflict(G):
    graph = []
    graph.append(Node("epsilon"))
    exists_conflicts, conflicts, table = table_analize(G)

    _ = build_graph(G, G.start_symbol, graph, table, [])

    if exists_conflicts:
        chain = build_chain(G, graph, conflicts)
    return chain


def build_graph(G, actual, graph, table, pending):
    if actual.is_epsilon:
        v = graph[0]
        if len(pending) > 0:
            if len(pending) > 1:
                pending = pending[1:len(pending)]
            else:
                pending = []

            new_node = build_graph(G, actual, graph, table, pending)
            if not v in new_node.adj and v != new_node:
                new_node.adj.append(v)
                v.adj.append(new_node)
        return v

    for v in graph:
        if actual.name == v.rep:
            if len(pending) > 0:
                if len(pending) > 1:
                    pending = pending[1:len(pending)]
                else:
                    pending = []

                new_node = build_graph(G, actual, graph, table, pending)

                if not v in new_node.adj and v != new_node:
                    new_node.adj.append(v)
                    v.adj.append(new_node)
            return v

    if actual.is_terminal:
        node = Node(actual.name, actual.name)
        graph.append(node)

        if len(pending) > 0:
            actual = pending[0]
            if len(pending) > 1:
                newpending = pending[1:len(pending)]
            else:
                newpending = []

            new_node = build_graph(G, actual, graph, table, newpending)
            if not node in new_node.adj and node != new_node:
                new_node.adj.append(node)
                node.adj.append(new_node)

        return node

    node = Node(actual.name)
    graph.append(node)
    for key in table:
        r, _ = key
        if r == actual:
            for item in table[key]:

                if (item.right.is_epsilon):
                    new_node = build_graph(G, symbols[0], graph, table,
                                           newpending)
                    if not node in new_node.adj and node != new_node:
                        new_node.adj.append(node)
                        node.adj.append(new_node)
                    continue

                symbols = item.right._symbols

                if len(symbols) > 0:
                    newpending = list(symbols[1:len(symbols)]) + pending
                new_node = build_graph(G, symbols[0], graph, table, newpending)
                if not node in new_node.adj and node != new_node:
                    new_node.adj.append(node)
                    node.adj.append(new_node)

    return node


class Node:
    def __init__(self, represent, write=""):
        self.adj = []
        self.rep = represent
        self.write = write

    def __str__(self):
        return self.rep

    def __repr__(self):
        return self.rep


def build_chain(G, graph, conflicts):

    for n in graph:
        if n.rep == str(conflicts[0][0][0]):
            init_node = n
        if n.rep == str(G.start_symbol):
            dest_node = n

    Q = [init_node]
    d = {}
    pi = {}
    for v in graph:
        d[v] = -1
        pi[v] = -1

    d[init_node] = 0

    while len(Q) > 0:
        u = Q.pop(0)
        for v in u.adj:
            if d[v] == -1:
                d[v] = d[u] + 1
                pi[v] = u
                Q.append(v)

    chain = ""
    actual = dest_node
    while (actual != -1):
        chain = chain + actual.write
        actual = pi[actual]

    chain = chain + str(conflicts[0][0][1])
    return chain


class TreeNode:
    def __init__(self, rep):
        self.adj = []
        self.rep = rep
