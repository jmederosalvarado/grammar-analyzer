import streamlit as st
from pandas import DataFrame
from grammar_analyzer.ll_analyzer import (
    is_ll_grammar,
    build_ll_table,
    build_conflict_str,
    get_derivation_tree_builder,
)

# pylint: disable=no-value-for-parameter


def run_ll_analysis(grammar):
    st.write("## LL Analysis")
    st.write("")

    is_ll = is_ll_grammar(grammar)
    st.write(f"__Your grammar is {'' if is_ll else 'not '} LL__")

    table = build_ll_table(grammar)
    st.write("__Parsing Table:__", table_to_dataframe(table))

    if is_ll:
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


# TODO: Refactor table to dataframe in various files


def table_to_dataframe(table):
    d = {}
    for (nt, t), value in table.items():
        value = [str(v) for v in value]
        try:
            d[nt][t] = value
        except KeyError:
            d[nt] = {t: value}

    return DataFrame.from_dict(d, orient="index", dtype=str)

