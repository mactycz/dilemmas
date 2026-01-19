import streamlit as st
from translations import init_language, language_selector,get_text
st.set_page_config(page_title="Dylematy")
init_language()
language_selector()

lang = st.session_state.language

start_page = st.Page("pages/choose.py", title=get_text("select_set",lang))
create_page = st.Page("pages/add.py", title=get_text("add_question",lang))
preview_page = st.Page("pages/preview.py", title=get_text("edit_questions",lang))

nav = st.navigation([start_page, create_page, preview_page])
nav.run()