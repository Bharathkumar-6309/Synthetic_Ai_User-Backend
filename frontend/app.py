import streamlit as st
from config import APP_NAME, APP_ICON
from utils.state_manager import init_session_state
from styles.theme import load_css

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

css = load_css("styles/custom.css")
if css:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.sidebar.title(f"{APP_ICON} {APP_NAME}")
st.sidebar.caption("Validate products without real users")
st.sidebar.divider()
st.sidebar.info(
    "Use the pages in the sidebar to move through the workflow:\n\n"
    "1. Experiment Workspace\n"
    "2. Persona Gallery\n"
    "3. Survey / Interview Mode\n"
    "4. Insights Dashboard\n"
    "5. Report Generator"
)

st.switch_page("pages/0_Home.py")
