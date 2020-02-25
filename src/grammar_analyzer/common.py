import pydot


def build_derivation_tree(parse, is_right_parse=False):
    parse = iter(parse)
    tree = pydot.Dot(graph_type="graph")
    __build_derivation_tree(tree, parse, is_right_parse)
    return tree


def __build_derivation_tree(tree, parse, is_right_parse, i=0):
    left, right = next(parse)
    body = reversed(right) if is_right_parse else right

    node = pydot.Node(i, label=left.name)
    tree.add_node(node)

    if len(body) == 0:
        child = pydot.Node(i + 1, label="eps")
        tree.add_node(child)
        tree.add_edge(pydot.Edge(node, child))

    for s in body:
        if s.is_terminal:
            child = pydot.Node(i + 1, label=s.name)
        else:
            child = __build_derivation_tree(tree, parse, is_right_parse, i + 1)

        tree.add_node(child)
        tree.add_edge(pydot.Edge(node, child))
        i += 1

    return node
