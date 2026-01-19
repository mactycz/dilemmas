import streamlit as st
TRANSLATIONS = {
    'pl': {
        'dilemmas':"Dylematy",

        # Navigation
        'select_set': 'Wybierz zestaw',
        'view_questions': 'Zobacz pytania',
        'add_question': 'Dodaj pytanie',
        'edit_questions': 'Edytuj pytania',
        
        # Buttons
        'export_pdf': 'Eksportuj do PDF',
        'download_pdf': '📄 Pobierz PDF',
        'save_changes': 'Zapisz zmiany',
        'cancel': 'Anuluj',
        'add': 'Dodaj',
        'new_set':"Nowy zestaw",
        'load_set':"Załaduj zestaw",

        # Labels
        'question': 'Pytanie',
        'option_a': 'Opcja A',
        'option_b': 'Opcja B',
        'question_number': 'Pytanie',
        
        # Messages
        'select_set_first': 'Najpierw wybierz zestaw!',
        'no_questions': 'Brak pytań w tym zestawie',
        'question_added': 'Pytanie zostało dodane!',
        'all_fields_required': 'Wszystkie pola muszą być wypełnione!',
        'char_limit_exceeded': 'Przekroczono limit znaków!',
        'no_questions_to_export': 'Brak pytań do eksportu',
        'db_error': 'Błąd przy otwieraniu bazy danych',
        'set_set_name':'Podaj nazwę zestawu',
        'name_set':'Nazwa zestawu',
        'choose_existing_set':'Wybierz istniejący zestaw',
        'set_not_existing':'Zestaw nie istnieje',

        # Character limits
        'max_chars': 'Maksymalnie {max} znaków',
        'chars_count': '{count}/{max} znaków',
        
        # Titles
        'questions_from_set': 'Pytania z zestawu:',
        'add_new_question': 'Dodaj nowe pytanie',
    },
    'en': {
        "dilemmas":"Dilemmas",
        # Navigation
        'select_set': 'Select Set',
        'view_questions': 'View Questions',
        'add_question': 'Add Question',
        'edit_questions': 'Edit Questions',
        
        
        # Buttons
        'export_pdf': 'Export to PDF',
        'download_pdf': '📄 Download PDF',
        'save_changes': 'Save Changes',
        'cancel': 'Cancel',
        'add': 'Add',
        'new_set':"New set",
        'load_set':"Load a set",

        # Labels
        'question': 'Question',
        'option_a': 'Option A',
        'option_b': 'Option B',
        'question_number': 'Question',
        
        # Messages
        'select_set_first': 'Please select a set first!',
        'no_questions': 'No questions in this set',
        'question_added': 'Question has been added!',
        'all_fields_required': 'All fields must be filled!',
        'char_limit_exceeded': 'Character limit exceeded!',
        'no_questions_to_export': 'No questions to export',
        'db_error': 'Error opening database',
        'set_set_name':'Set a name for the set',
        'name_set':'Name of the set',
        'choose_existing_set':'Choose existing set',
        'set_not_existing':'Set does not exist',

        # Character limits
        'max_chars': 'Maximum {max} characters',
        'chars_count': '{count}/{max} characters',
        
        # Titles
        'questions_from_set': 'Questions from set:',
        'add_new_question': 'Add New Question',
    }
}
def get_text(key, lang='pl', **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS['pl']).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


def init_language():
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'


def language_selector():
    with st.sidebar:
        st.divider()
        lang = st.radio(
            "🌍 Language / Język",
            options=['pl', 'en'],
            format_func=lambda x: '🇵🇱 Polski' if x == 'pl' else '🇬🇧 English',
            key='language'
        )