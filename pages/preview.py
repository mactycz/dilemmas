import streamlit as st
import pandas as pd
import sqlite3
from loading import check_changes
from printing import create_printable_pdf

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'db' not in st.session_state or st.session_state.db is None:
    st.warning("Najpierw wybierz zestaw!")
    st.stop()
db = st.session_state.db


try:
    conn = sqlite3.connect(f'{db}.db')
    df = pd.read_sql_query("SELECT question, option_A, option_B FROM dilemas", conn)
    conn.close()
except Exception as e:
    st.error(f"Błąd przy otwieraniu bazy danych: {e}")
    st.stop()

if df.empty:
    st.info("Brak pytań w tym zestawie")
else:
    st.title(f"Pytania z zestawu: {st.session_state.db}")
    df.columns = ['Pytanie', 'Opcja A', 'Opcja B']
    editor =st.data_editor(df, hide_index=True, num_rows="dynamic", disabled=not st.session_state.edit_mode, key="questions_editor")


if st.session_state.edit_mode:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Anuluj"):
            st.session_state.edit_mode = False
            st.session_state.pop("questions_editor", None)
            st.rerun()

    with col2:
        if st.button("Zapisz zmiany"):
            check_changes(editor, db)
            st.session_state.edit_mode = False
            st.session_state.pop("questions_editor", None)
            st.rerun()
else:
    if st.button("Edytuj pytania"):
        st.session_state.edit_mode = True
        st.session_state.pop("questions_editor", None) 
        st.rerun()

if st.button('Eksportuj do pdf'):
    if not df.empty:
        pdf_buffer = create_printable_pdf(df)
        st.download_button(
            label="Pobierz PDF",
            data=pdf_buffer,
            file_name=f"{db}_pytania.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Brak pytań do eksportu")