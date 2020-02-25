from functools import namedtuple

shift_reduce_info = namedtuple(
    "parser_info",
    ("automaton", "action_table", "goto_table", "shift_act", "reduce_act"),
)


def build_conflict_str(action, goto, terminals, shift_act, reduce_act):
    return __build_conflict_str(
        [0], set(), action, goto, terminals, shift_act, reduce_act
    )


def __build_conflict_str(
    stack, visited, action_table, goto_table, terminals, shift_act, reduce_act
):
    state = stack[-1]

    for t in terminals:
        if (state, t) in visited:
            continue

        try:
            value = action_table[state, t]
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
            if conflict is None:
                continue
            return [t] + conflict

        if action == reduce_act:
            visited.add((state, t))
            temp_stack = stack[: -len(tag.right)]
            return __build_conflict_str(
                temp_stack + [goto_table[temp_stack[-1], tag.left][0]],
                visited,
                action_table,
                goto_table,
                terminals,
                shift_act,
                reduce_act,
            )

    return None
