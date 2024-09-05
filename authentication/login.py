import streamlit as st
from bcrypt import checkpw
import pickle

def get_hashed_password(username):
    try:
        with open('authentication/hashed_passwords.pkl', 'rb') as file:
            hashed_passwords = pickle.load(file)
        return hashed_passwords.get(username)
    except FileNotFoundError:
        return None

def login():
    st.image("assets/file.png", width=450)
    st.write("Please log in to access the dashboard.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        hashed_password = get_hashed_password(username)
        if hashed_password and checkpw(password.encode(), hashed_password):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.page = "Dashboard"  
        else:
            st.error("Invalid username or password")
with open('css/styles.css') as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
