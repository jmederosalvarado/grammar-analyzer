from pycmp.parsing import SLR1Parser


class SLR1ParserConflicts(SLR1Parser):
    def __call__(self, tokens, return_actions=False):
        raise NotImplementedError()

    @staticmethod
    def _register(table, key, value):
        if key in table and value not in table[key]:
            table[key].append(value)
        else:
            table[key].append(value)


def build_conflict_str(action, goto, terminals, shift_act, reduce_act):
    return __build_conflict_str(
        [0], set(), action, goto, terminals, reduce_act, reduce_act
    )


def __build_conflict_str(
    stack, visited, action_table, goto_table, terminals, shift_act, reduce_act
):
    state = stack[-1]

    for t in terminals:
        if (state, t) in visited:
            continue

        try:
            value = action[state, t]
        except KeyError:
            continue

        if len(value) > 1:
            return [t]

        action, tag = value[0]

        if action == shift_act:
            visited.add((state, t))
            conflict = __build_conflict_str(
                stack + [tag],
                visited,
                action_table,
                goto_table,
                terminals,
                shift_act,
                reduce_act,
            )
            visited.remove((state, t))
            if conflict is None:
                return None
            return [t] + conflict

        if action == reduce_act:
            visited.add((state, t))
            temp_stack = stack[: -len(tag.right)]
            conflict = __build_conflict_str(
                temp_stack + [goto_table[temp_stack[-1], tag.left]],
                visited,
                action_table,
                goto_table,
                terminals,
                shift_act,
                reduce_act,
            )
            visited.remove((state, t))
            return conflict

    return None
