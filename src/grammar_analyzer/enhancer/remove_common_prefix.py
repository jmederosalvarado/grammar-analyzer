from pycmp.grammar import Grammar, Sentence, Symbol
from itertools import islice


# Α trie structure implementation so we can find common prefixes in the grammar productions
class TrieNode:
    def __init__(self, depth=-1, parent=None, symbol=None):
        self.children = {}
        self.depth = depth
        self.parent = parent
        self.symbol = symbol
        self.productions = []


class Trie:
    def __init__(self, symbol):
        self.root = TrieNode()
        self.prefix_nodes = (
            set()
        )  # set that contains nodes where ends one largest common prefix of at least two productions
        self.symbol = symbol
        for p in symbol.productions:
            self.add(p)

    def add(self, production):
        node = self.root
        for s in production.right:
            try:
                node = node.children[s]
            except KeyError:
                node.children[s] = TrieNode(node.depth + 1, node, s)
                if (len(node.children) == 2
                        and node.parent) or node.productions:
                    self.prefix_nodes.add(node)
                node = node.children[s]

        node.productions.append(production)
        if len(node.children) >= 1:
            self.prefix_nodes.add(node)

    def get_node_productions(self, node: TrieNode):
        productions = [p for p in node.productions]
        for k in node.children:
            productions += self.get_node_productions(node.children[k])
        return productions


def remove_common_prefixes(G: Grammar):
    for A in G.nonterminals.copy():
        count = 1
        trie = Trie(A)
        prefix_nodes = [n for n in trie.prefix_nodes]
        prefix_nodes.sort(key=lambda x: x.depth, reverse=True)

        for (n) in (
                prefix_nodes
        ):  # get the longest common prefix among the productions be the prefix α
            productions = trie.get_node_productions(
                n)  # get all the productions with that prefix
            n.children.clear()

            #A -> α ω1 | α ω2 | ... | α ωΝ
            #replace those productions with
            #A -> αA'
            #A' -> ω1 | ω2 | ... | ωΝ

            A_new = G.add_nonterminal(A.name + ("'" * count), False)
            count += 1
            A %= Sentence(*islice(productions[0].right, 0, n.depth +
                                  1)) + A_new
            n.productions = [A.productions[-1]]

            for p in productions:
                if len(p.right) > n.depth + 1:
                    A_new %= Sentence(*islice(p.right, n.depth + 1, None))
                else:
                    A_new %= G.epsilon
                A.productions.remove(p)
                G.productions.remove(p)
