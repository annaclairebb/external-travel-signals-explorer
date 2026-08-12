"""Streamlit entry point for the External Travel Signals Explorer."""

import streamlit as st

from webapp.data import DataValidationError, load_app_data
from webapp.navigation import render_navigation
from webapp.styles import apply_styles


st.set_page_config(
    page_title="External Travel Signals Explorer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

try:
    _app_data = load_app_data()
except (DataValidationError, ImportError, OSError, ValueError) as error:
    st.error(
        "The app could not load its evidence sources. "
        "Check the local data files and model dependencies."
    )
    st.exception(error)
    st.stop()

render_navigation()
