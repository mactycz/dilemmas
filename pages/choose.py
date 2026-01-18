import streamlit as st
import sqlite3
import json
import os
from loading import *

if 'db' not in st.session_state:
    st.session_state.db = None
st.title('Dylematy')
text = st.text_input("Podaj nazwę zestawu",placeholder = 'Nazwa zestawu')

if st.button("Nowe zestaw dylematów"):
    if text:
        init_db(text)
        add_to_sets(text)
    else:
        st.warning("Podaj nazwę zestawu")

option = st.selectbox(
    "Wybierz istniejący zestaw:",
    options
)


if st.button("Załaduj zestaw"):
    if option:
        init_db(option)
    else:
        st.warning("Taki zestaw nie istnieje")
