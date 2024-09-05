import pickle
import os
import streamlit as st

SESSION_FILE = 'session.pkl'

def create_session(username):
    session_data = {'username': username}
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump(session_data, f)

def check_session():
    return st.session_state.get('logged_in', False)

def get_username():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'rb') as f:
            session_data = pickle.load(f)
            return session_data.get('username')
    return None

def logout():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
