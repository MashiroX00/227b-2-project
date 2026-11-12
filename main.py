from services.markov_services import load_sentences

def main():
    print("Hello from 227b-2-project!")
import streamlit as st

# Config Streamlit 
st.set_page_config(page_title="Group 2", layout="wide", initial_sidebar_state="expanded")
st.title("Group 2 - Streamlit App")
st.markdown("----")

if __name__ == "__main__":
    main()

# Pages Config and prefix
bayes_page = st.Page("./pages/bayes_page.py", title="Bayes Theorem", icon="📊")
statistics_page = st.Page("./pages/statistics.py", title="Statistics Calculator", icon="📈")
markov_page = st.Page("./pages/markov.py", title="Markov Chain", icon="🔗")
custom_page = st.Page("./pages/custom_app.py", title="Chat Moderator (Custom)", icon="🗨️")
terrain_page = st.Page("./pages/terrain_page.py", title="Terrain Generator", icon="⛰️")

pages = {
    "App": [bayes_page, statistics_page, markov_page, custom_page, terrain_page],
}

# Navigation
nv = st.navigation(pages)
nv.run()
