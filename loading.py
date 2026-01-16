import streamlit as st
import sqlite3
import json
import os
import pandas as pd

if os.path.exists('sets.json'):
    with open('sets.json', 'r', encoding='utf-8') as f:
        options = json.load(f)
else:
    options = []

def add_to_sets(name):
    if os.path.exists('sets.json'):
        with open('sets.json', 'r', encoding='utf-8') as f:
            sets = json.load(f)
    else:
        sets = []
    if name not in sets:
        sets.append(name)

    with open('sets.json', 'w', encoding='utf-8') as f:
        json.dump(sets, f, ensure_ascii=False, indent=2)


def init_db(name):
    conn = sqlite3.connect(f'{name}.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dilemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL CHECK(length(question) <= 256),
            option_A TEXT NOT NULL CHECK(length(option_A) <= 128),
            option_B TEXT NOT NULL CHECK(length(option_B) <= 128)
        )
    ''')
    st.session_state.db = name
    conn.commit()
    conn.close()


def add_dilema(db_name, question, option_A, option_B):
    conn = sqlite3.connect(f'{db_name}.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO dilemas (question, option_A, option_B)
        VALUES (?, ?, ?)
    ''', (question,option_A, option_B))
    conn.commit()
    conn.close()

def delete_row(db_name, row_id):
    conn = sqlite3.connect(f'{db_name}.db')
    c = conn.cursor()
    c.execute('DELETE FROM dilemas WHERE id = ?', (row_id,))
    conn.commit()
    conn.close()

def check_changes(edited_df, db):
    conn = sqlite3.connect(f"{db}.db")
    c = conn.cursor()

    c.execute("DELETE FROM dilemas")

    for _, row in edited_df.iterrows():
        if pd.notna(row["Pytanie"]) and str(row["Pytanie"]).strip():
            c.execute(
                "INSERT INTO dilemas (question, option_A, option_B) VALUES (?, ?, ?)",
                (row["Pytanie"], row["Opcja A"], row["Opcja B"])
            )

    conn.commit()
    conn.close()
