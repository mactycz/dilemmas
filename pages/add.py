import streamlit as st
import sqlite3
from translations import get_text

lang = st.session_state.language

if 'db' not in st.session_state or st.session_state.db is None:
    st.warning(get_text('select_set_first', lang))
    st.stop()

db = st.session_state.db

st.title(get_text('add_new_question', lang))

question = st.text_area(
    get_text('question', lang), 
    max_chars=256,
    help=get_text('max_chars', lang, max=256)
)
st.caption(get_text('chars_count', lang, count=len(question), max=256))

option_a = st.text_input(
    get_text('option_a', lang), 
    max_chars=128,
    help=get_text('max_chars', lang, max=128)
)
st.caption(get_text('chars_count', lang, count=len(option_a), max=128))

option_b = st.text_input(
    get_text('option_b', lang), 
    max_chars=128,
    help=get_text('max_chars', lang, max=128)
)
st.caption(get_text('chars_count', lang, count=len(option_b), max=128))

if st.button(get_text('add_question', lang)):
    if not question or not option_a or not option_b:
        st.error(get_text('all_fields_required', lang))
    else:
        try:
            conn = sqlite3.connect(f'{db}.db')
            conn.text_factory = str  # UTF-8 support
            c = conn.cursor()
            c.execute(
                "INSERT INTO dilemas (question, option_A, option_B) VALUES (?, ?, ?)",
                (question, option_a, option_b)
            )
            conn.commit()
            conn.close()
            st.success(get_text('question_added', lang))
            st.rerun()
        except sqlite3.IntegrityError:
            st.error(get_text('char_limit_exceeded', lang))
        except Exception as e:
            st.error(f"{get_text('db_error', lang)}: {e}")