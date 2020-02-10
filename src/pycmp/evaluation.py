from pycmp.grammar import EOF
from pycmp.parsing import ShiftReduceParser


def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).ttype, EOF)
    return result


def evaluate(production, left_parse, tokens, inherited_value=None):
    _, body = production
    attributes = production.attributes

    synteticed = [None]
    inherited = [inherited_value]

    for i, symbol in enumerate(body, 1):
        inherited.append(attributes[i] and attributes[i](inherited, synteticed))
        if symbol.is_terminal:
            assert inherited[i] is None
            lex = next(tokens).lex
            synteticed.append(lex)
        else:
            next_production = next(left_parse)
            assert symbol == next_production.left
            synteticed.append(
                evaluate(next_production, left_parse, tokens, inherited[i])
            )

    synteticed[0] = attributes[0] and attributes[0](inherited, synteticed)
    return synteticed[0]


def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            _, body = production
            attributes = production.attributes
            assert all(
                rule is None for rule in attributes[1:]
            ), "There must be only synteticed attributes."
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body) :]
                value = rule(None, synteticed)
                stack[-len(body) :] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception("Invalid action!!!")

    assert len(stack) == 1
    assert isinstance(next(tokens).ttype, EOF)
    return stack[0]
