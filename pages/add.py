import streamlit as st
import sqlite3

if 'db' not in st.session_state or st.session_state.db is None:
    st.warning("Najpierw wybierz zestaw!")
    st.stop()

db = st.session_state.db

st.title("Dodaj nowe pytanie")

question = st.text_area(
    "Pytanie", 
    max_chars=256,
    help="Maksymalnie 256 znaków"
)
st.caption(f"{len(question)}/256 znaków")

option_a = st.text_input(
    "Opcja A", 
    max_chars=128,
    help="Maksymalnie 128 znaków"
)
st.caption(f"{len(option_a)}/128 znaków")

option_b = st.text_input(
    "Opcja B", 
    max_chars=128,
    help="Maksymalnie 128 znaków"
)
st.caption(f"{len(option_b)}/128 znaków")

if st.button("Dodaj pytanie"):
    if not question or not option_a or not option_b:
        st.error("Wszystkie pola muszą być wypełnione!")
    else:
        try:
            conn = sqlite3.connect(f'{db}.db')
            conn.text_factory = str
            c = conn.cursor()
            c.execute(
                "INSERT INTO dilemas (question, option_A, option_B) VALUES (?, ?, ?)",
                (question, option_a, option_b)
            )
            conn.commit()
            conn.close()
            st.success("Pytanie zostało dodane!")
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Przekroczono limit znaków!")
        except Exception as e:
            st.error(f"Błąd: {e}")