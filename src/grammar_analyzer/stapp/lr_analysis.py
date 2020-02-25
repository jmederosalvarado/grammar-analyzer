import streamlit as st
from pandas import DataFrame
from grammar_analyzer.lr_analyzer import (
    is_lr_grammar,
    build_conflict_str,
    build_automaton,
    build_lr_tables,
    get_derivation_tree_builder,
)

# pylint: disable=no-value-for-parameter


def run_lr_analysis(grammar):
    st.write("## LR analysis")
    st.write("")

    is_lr = is_lr_grammar(grammar)
    st.write(f"__Your grammar is {'' if is_lr else 'not '} LR__")

    action, goto = build_lr_tables(grammar)
    st.write("__ACTION:__", table_to_dataframe(action))
    st.write("__GOTO:__", table_to_dataframe(goto))

    if not is_lr:
        conflict = build_conflict_str(grammar)
        conflict = " ".join(str(t) for t in conflict)
        st.write(
            "A possible string that leads to a conflict when trying to parse it is:"
        )
        st.write(f"> __{conflict.strip()}__ ...")

    # automaton = build_automaton(grammar)
    # st.write("__LR0 Automaton:__")
    # st.graphviz_chart(str(automaton))


def encode_value(value):
    try:
        action, tag = value
        if action == "SHIFT":
            return "S" + str(tag)
        elif action == "REDUCE":
            return repr(tag)
        elif action == "OK":
            return action
        else:
            return value
    except TypeError:
        return value


def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = [encode_value(v) for v in value]
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = {symbol: value}

    return DataFrame.from_dict(d, orient="index", dtype=str)
