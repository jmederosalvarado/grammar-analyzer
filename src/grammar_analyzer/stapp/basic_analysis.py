import streamlit as st
from grammar_analyzer.basic_analyzer import compute_firsts, compute_follows
from pycmp.utils import ContainerSet

# pylint: disable=no-value-for-parameter


def run_basic_analysis(grammar):
    st.write("## Basic analysis")
    st.write("")

    firsts = compute_firsts(grammar)
    st.write("__Firsts:__", {str(k): str(v) for k, v in firsts.items()})

    follows = compute_firsts(grammar)
    st.write("__Follows:__", {str(k): str(v) for k, v in follows.items()})

