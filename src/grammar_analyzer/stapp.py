import streamlit as st
from grammar_analyzer.interpreter import eval_input
from grammar_analyzer.stutils import stformat

# pylint: disable=no-value-for-parameter


def basic_analysis(grammar):
    pass


def ll_analysis(grammar):
    pass


def slr_analysis(grammar):
    pass


def lr_analysis(grammar):
    pass


def regular_analysis(grammar):
    pass


def enhacement_analysis(grammar):
    pass


def input_grammar():
    input_text = st.text_area(
        label="Please input your grammar here",
        value="balanced -> ( balanced ) | balanced ( ) | ( ) balanced | eps",
    )
    grammar = eval_input(input_text)
    return grammar


def build_options():
    return {
        "Basic": basic_analysis,
        "LL": ll_analysis,
        "SLR": slr_analysis,
        "LR": lr_analysis,
        "Regular": regular_analysis,
        "Enhancement": enhacement_analysis,
    }


def run():
    st.title("Grammar Analyzer")

    grammar = input_grammar()

    if grammar is None:
        return

    options = build_options()

    option = st.selectbox(
        label="Select type of analysis to be made", options=tuple(options),
    )

    function = options[option]
    function(grammar)


if __name__ == "__main__":
    run()
