from .grammar import EOF


def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).token_type, EOF)
    return result


def evaluate(production, left_parse, tokens, inherited_value=None):
    _, body = production
    attributes = production.attributes

    synteticed = [None]
    inherited = [inherited_value]

    for i, symbol in enumerate(body, 1):
        inherited.append(attributes[i] and attributes[i](inherited, synteticed))
        if symbol.IsTerminal:
            assert inherited[i] is None
            lex = next(tokens).lex
            synteticed.append(lex)
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            synteticed.append(evaluate(next_production, left_parse, tokens, inherited[i]))

    synteticed[0] = attributes[0] and attributes[0](inherited, synteticed)
    return synteticed[0]
