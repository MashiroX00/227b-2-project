import streamlit as st

# Config Streamlit 
st.set_page_config(page_title="Group 2", layout="wide", initial_sidebar_state="expanded")
st.title("Group 2 - Streamlit App")
st.markdown("----")

# Pages Config and prefix
bayes_page = st.Page("./pages/bayes_page.py", title="Bayes Theorem", icon="📊")
statistics_page = st.Page("./pages/statistics.py", title="Statistics Calculator", icon="📈")

pages = {
    "App": [bayes_page, statistics_page],
}

# Navigation
nv = st.navigation(pages)
nv.run()