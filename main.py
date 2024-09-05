import streamlit as st


st.set_page_config(
    page_title="Smart Energy & Sustainability Dashboard", 
    page_icon="assets/icon.png",  
    layout="centered"  
)

from authentication.login import login
from authentication.register import register
from dashboard.dashboard import dashboard

def main():


    page = st.sidebar.radio("Select Page", ["Login", "Sign Up", "Dashboard"], format_func=lambda x: f"🔑 {x}" if x == "Login" else f"📝 {x}" if x == "Sign Up" else f"🌦️ {x}")

    if page == "Login":
        login()
    elif page == "Sign Up":
        register()
    elif page == "Dashboard":
        if 'logged_in' in st.session_state and st.session_state.logged_in:
            dashboard()
        else:
            st.warning("Please log in to access the dashboard.")

if __name__ == '__main__':
    main()


with open('styles.css') as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
