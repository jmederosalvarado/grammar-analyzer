import streamlit as st
from grammar_analyzer.regular_analyzer import (
    is_regular_grammar,
    grammar_to_automaton,
    automaton_to_regex,
)

# pylint: disable=no-value-for-parameter


def run_regular_analysis(grammar):
    st.write("## Regular Language Analysis")
    st.write("")

    is_regular = is_regular_grammar(grammar)
    st.write(f"__Your grammar is {'' if is_regular else 'not '} Regular__")

    if not is_regular:
        return

    automaton = grammar_to_automaton(grammar)
    st.graphviz_chart(str(automaton.graph()))

    regex = automaton_to_regex(automaton)
    st.write(f"_A regular expression to represent your grammar could be:_")
    st.write(f"> {regex}")
    st.write("where '@' doesn't match any symbol in your vocabulary")
