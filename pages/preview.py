import streamlit as st
import pandas as pd
import sqlite3
from loading import check_changes
from printing import create_printable_pdf
from translations import get_text
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
lang = st.session_state.language
if 'db' not in st.session_state or st.session_state.db is None:
    st.warning(get_text("select_set_first",lang))
    st.stop()
db = st.session_state.db


try:
    conn = sqlite3.connect(f'{db}.db')
    df = pd.read_sql_query("SELECT question, option_A, option_B FROM dilemas", conn)
    conn.close()
except Exception as e:
    st.error(get_text('db_error',lang)+" "+e)
    st.stop()

if df.empty:
    st.info(get_text("no_questions",lang))
else:
    st.title(get_text("questions_from_set",lang)+" "+st.session_state.db)
    df.columns = [get_text('question',lang), get_text('option_a',lang), get_text('option_b',lang)]
    editor =st.data_editor(df, hide_index=True, num_rows="dynamic", disabled=not st.session_state.edit_mode, key="questions_editor")


if st.session_state.edit_mode:
    col1, col2 = st.columns(2)

    with col1:
        if st.button(get_text('cancel',lang)):
            st.session_state.edit_mode = False
            st.session_state.pop("questions_editor", None)
            st.rerun()

    with col2:
        if st.button(get_text('save_changes',lang)):
            check_changes(editor, db)
            st.session_state.edit_mode = False
            st.session_state.pop("questions_editor", None)
            st.rerun()
else:
    if st.button(get_text('edit_questions',lang)):
        st.session_state.edit_mode = True
        st.session_state.pop("questions_editor", None) 
        st.rerun()

if st.button(get_text('export_pdf',lang)):
    if not df.empty:
        pdf_buffer = create_printable_pdf(df)
        st.download_button(
            label=get_text('download_pdf',lang),
            data=pdf_buffer,
            file_name=f"{db}_pytania.pdf",
            mime="application/pdf"
        )
    else:
        st.warning(get_text('no_questions_to_export',lang))