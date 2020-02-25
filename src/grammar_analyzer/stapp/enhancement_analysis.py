import streamlit as st
from grammar_analyzer.enhancer import (
    remove_left_recursion,
    remove_unnecesary_productions,
    remove_common_prefixes,
)

# pylint: disable=no-value-for-parameter


def run_enhancement_analysis(grammar):
    st.write("## Enhancement of grammar")
    st.write("")

    no_left_recursion = remove_left_recursion(grammar)
    st.write("__Grammar without left recursion:__")
    st.write(grammar_to_str(no_left_recursion))

    no_unnecesary_productions = remove_unnecesary_productions(grammar)
    st.write("__Grammar without unnecesary productions:__")
    st.write(grammar_to_str(no_unnecesary_productions))

    # no_common_prefixes = remove_common_prefixes(grammar)
    # st.write("__Grammar without common prefixes:__")
    # st.write(grammar_to_str(no_common_prefixes))


def grammar_to_str(grammar):
    return "\n".join((f"> {left} -> {right if len(right) else 'eps'}\n")
                     for left, right in grammar.productions)
