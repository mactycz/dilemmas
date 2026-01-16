import streamlit as st

st.set_page_config(page_title="Dylematy")

start_page = st.Page("pages/choose.py", title="Wybierz zestaw")
create_page = st.Page("pages/add.py", title="Dodaj dylemat")
preview_page = st.Page("pages/preview.py", title="Zarządzaj dylematami")

nav = st.navigation([start_page, create_page, preview_page])
nav.run()