import streamlit as st
from grammar_analyzer.interpreter import eval_input
from grammar_analyzer.stapp.basic_analysis import run_basic_analysis
from grammar_analyzer.stapp.ll_analysis import run_ll_analysis
from grammar_analyzer.stapp.slr_analysis import run_slr_analysis
from grammar_analyzer.stapp.lr_analysis import run_lr_analysis
from grammar_analyzer.stapp.regular_analysis import run_regular_analysis
from grammar_analyzer.stapp.enhancement_analysis import run_enhancement_analysis

# pylint: disable=no-value-for-parameter


def input_grammar():
    input_text = st.text_area(
        label="Please input your grammar here",
        value="s -> if x then s\ns -> if x then s else s\ns -> num\nx -> num",
    )
    try:
        return eval_input(input_text)
    except:
        return None


def build_options():
    return {
        "Basic": run_basic_analysis,
        "LL": run_ll_analysis,
        "SLR": run_slr_analysis,
        "LR": run_lr_analysis,
        "Regular": run_regular_analysis,
        "Enhancement": run_enhancement_analysis,
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
