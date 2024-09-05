import streamlit as st
import streamlit_shadcn_ui as ui
from authentication.session_management import check_session, get_username, logout
from functions.weather import display_weather_data
from functions.prediction import predictions
from chat.chatbot import chatbot_page
from authentication.logout import logout

def dashboard():
    if not check_session():
        st.error("You are not logged in. Please log in to access the dashboard.")
        return

    username = get_username()

    st.title("Smart Energy & Sustainability Dashboard")
    st.write("##")
    ui.badges(badge_list=[("Welcome", "default"), ("Back", "secondary"), 
                          ("!!", f"{username}"), ("!!", "destructive")])

    st.write("## About This App 🌍")
    st.write("""
    This app is designed to provide interactive insights into weather data ☀️, predictions 📊, and sustainability recommendations ♻️. 
    You can check the current weather conditions 🌦️, make predictions 🔮, and get expert advice on sustainability-related questions 💡. 

    Developed by Sami Khalfi, a third-year data science student at ESI 🎓. 
    Connect with me on [LinkedIn](https://www.linkedin.com/in/sami-khalfi-355098290/) 🔗.
    """)

    tab = ui.tabs(options=['Weather', 'Predictions', 'Chatbot', 'Logout'], 
                  default_value='Weather', key="kanaries")

    if tab == 'Weather':
        display_weather_data()  

    elif tab == 'Predictions':
        st.write("## Predictions")
        predictions()  

    elif tab == 'Chatbot':
        chatbot_page()

    elif tab == 'Logout':
        logout()

    # Apply custom CSS
    with open('css/styles.css') as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if __name__ == '__main__':
    dashboard()
