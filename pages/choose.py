import streamlit as st
import sqlite3
import json
import os
from loading import *
from translations import get_text

lang = st.session_state.language
if 'db' not in st.session_state:
    st.session_state.db = None
st.title(get_text("dilemmas",lang))
text = st.text_input(get_text("set_set_name",lang),placeholder =get_text("name_set",lang))

if st.button(get_text("new_set",lang)):
    if text:
        init_db(text)
        add_to_sets(text)
    else:
        st.warning(get_text("set_set_name",lang))

option = st.selectbox(
    get_text('choose_existing_set',lang),
    options
)


if st.button(get_text('load_set',lang)):
    if option:
        init_db(option)
    else:
        st.warning(get_text('set_not_existing'),lang)
