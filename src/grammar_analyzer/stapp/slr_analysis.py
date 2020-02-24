import streamlit as st
from grammar_analyzer.slr_analyzer import (
    is_slr_grammar,
    build_conflict_str,
    build_automaton,
)

# pylint: disable=no-value-for-parameter


def run_slr_analysis(grammar):
    st.write("## SLR analysis")
    st.write("")

    is_slr = is_slr_grammar(grammar)
    st.write(f"__Your grammar is {'' if is_slr else 'not '} SLR__")

    if not is_slr:
        conflict = build_conflict_str(grammar)
        st.write(
            "A possible string that leads to a conflict when trying to parse it is:"
        )
        st.write(conflict)

    automaton = build_automaton(grammar)
    st.graphviz_chart(str(automaton))
