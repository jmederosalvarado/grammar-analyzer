import pydot


def build_derivation_tree(parse, is_right_parse=False):
    parse = iter(parse)
    tree = pydot.Graph(graph_type="graph")
    return __build_derivation_tree(tree, parse, is_right_parse)


def __build_derivation_tree(tree, parse, is_right_parse):
    left, right = next(parse)
    node = pydot.Node(left.name)
    body = reversed(right) if is_right_parse else right
    for s in body:
        if s.is_terminal or s.is_epsilon:
            tree.add_edge(node, pydot.Node(s.name))
        else:
            child = __build_derivation_tree(tree, parse, is_right_parse)
            tree.add_edge(pydot.Edge(node, child))
    return node
