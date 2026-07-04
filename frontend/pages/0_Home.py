import streamlit as st
from config import APP_NAME, APP_ICON, APP_TAGLINE, USE_MOCK_DATA
from utils.state_manager import init_session_state, has_experiment

st.set_page_config(page_title="Home", page_icon=APP_ICON, layout="wide")
init_session_state()

if USE_MOCK_DATA:
    st.caption("🧪 Running in mock data mode — no real backend calls are being made.")

st.title(f"{APP_ICON} {APP_NAME}")
st.subheader(APP_TAGLINE)

col1, col2, col3 = st.columns(3)
col1.metric("Personas Generated", "500+")
col2.metric("Accuracy Rate", "98%")
col3.metric("Per Test Time", "15 min")

st.divider()

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 Start New Experiment", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Experiment_Workspace.py")
with c2:
    if st.button("📊 View Dashboard", use_container_width=True, disabled=not has_experiment()):
        st.switch_page("pages/5_Insights_Dashboard.py")
    if not has_experiment():
        st.caption("Create an experiment first to unlock the dashboard.")

st.divider()
st.markdown("### Recent Experiments")

recent = st.session_state.get("experiments_history", [])
if not recent:
    st.info("No experiments yet. Start your first one above!")
else:
    for exp in recent[-5:][::-1]:
        st.write(f"📱 **{exp['product_name']}** — {exp.get('would_use_pct', '?')}% would use")
