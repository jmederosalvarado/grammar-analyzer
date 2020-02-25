import streamlit as st
from pandas import DataFrame
from grammar_analyzer.slr_analyzer import (
    is_slr_grammar,
    build_conflict_str,
    build_automaton,
    build_slr_tables,
    get_derivation_tree_builder,
)

# pylint: disable=no-value-for-parameter


def run_slr_analysis(grammar):
    st.write("## SLR analysis")
    st.write("")

    is_slr = is_slr_grammar(grammar)
    st.write(f"__Your grammar is {'' if is_slr else 'not '} SLR__")

    action, goto = build_slr_tables(grammar)
    st.write("__ACTION:__", table_to_dataframe(action))
    st.write("__GOTO:__", table_to_dataframe(goto))

    automaton = build_automaton(grammar)
    st.write("__LR0 Automaton:__")
    st.graphviz_chart(str(automaton))

    if is_slr:
        tree_builder = get_derivation_tree_builder(grammar)
        string = st.text_input("Please enter a string to parse").split()
        if not string:
            return
        tree = tree_builder(string)
        st.graphviz_chart(str(tree))

    else:
        conflict = build_conflict_str(grammar)
        conflict = " ".join(str(t) for t in conflict)
        st.write(
            "A possible string that leads to a conflict when trying to parse it is:"
        )
        st.write(f"> __{conflict.strip()}__ ...")


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
