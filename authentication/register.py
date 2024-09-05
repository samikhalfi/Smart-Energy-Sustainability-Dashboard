import streamlit as st
from bcrypt import hashpw, gensalt
import pickle

def store_user_credentials(username, hashed_password):
    try:
        with open('hashed_passwords.pkl', 'rb') as file:
            hashed_passwords = pickle.load(file)
    except FileNotFoundError:
        hashed_passwords = {}

    if username in hashed_passwords:
        st.error("Username already exists. Please choose a different username.")
        return False

    hashed_passwords[username] = hashed_password

    with open('hashed_passwords.pkl', 'wb') as file:
        pickle.dump(hashed_passwords, file)
    
    return True

def register():
    st.image("assets/file.png", width=450)
    st.write("Create a new account")
    
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if username and password:
            hashed_password = hashpw(password.encode(), gensalt())
            if store_user_credentials(username, hashed_password):
                st.success("Registration successful! Please log in.")
                st.session_state.page = "Login" 
            else:
                st.error("Registration failed.")
        else:
            st.error("Please provide both username and password")
with open('css/styles.css') as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
