"""workbench.py — Streamlit entry point: the synthetic data page."""
import streamlit as st

from synthtool.app import synth_page

st.set_page_config(page_title="Synthetic data tool", page_icon=":material/science:", layout="wide")
synth_page.page()
