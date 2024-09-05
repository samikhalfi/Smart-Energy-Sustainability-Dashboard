import streamlit as st
import pandas as pd
import openai
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

def save_api_key(api_key: str):
    st.session_state.api_key = api_key

def get_chatbot_response(user_question: str, file_path: str = "assets/data.csv") -> str:
    if 'api_key' not in st.session_state or not st.session_state.api_key:
        st.warning("Please enter your OpenAI API key to use the chatbot.")
        return ""

    openai.api_key = st.session_state.api_key

    df = pd.read_csv(file_path)

    llm = ChatOpenAI(model="gpt-4o", temperature=0.3, openai_api_key=openai.api_key)
    agent_executor = create_pandas_dataframe_agent(
        llm,
        df,
        agent_type="tool-calling",
        verbose=True,
        allow_dangerous_code=True
    )

    detailed_prompt = (
        "Hello! I am a chatbot working for Smart Energy & Sustainability company, a specialized expert analyst designed to provide interactive insights into weather data, "
        "predictions, and sustainability recommendations. This app allows you to check the current weather conditions, "
        "make predictions, and get expert advice on sustainability-related questions. "
        "As an expert analyst, I can help you understand and interpret the CSV data you provide, offering valuable insights into electricity consumption patterns, weather conditions, and billing details. "
        "Developed by Sami Khalfi, a second-year data science student at ESI. Connect with Sami on [LinkedIn](https://www.linkedin.com/in/sami-khalfi-355098290/).\n\n"
        "If you have any questions or need help understanding the data, feel free to ask! Here is the context of the data you can work with:\n\n"
        f"{user_question}\n"
    )

    answer = agent_executor.run(detailed_prompt)
    return answer

def chatbot_page():
    st.write("## Chatbot")
    st.caption("🚀 A Streamlit chatbot powered by OpenAI with expertise in sustainability")

    if 'api_key' in st.session_state and st.session_state.api_key:
        st.write("You can now use the chatbot.")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_prompt = st.chat_input("Ask An Expert...")

        if user_prompt:
            st.chat_message("user").markdown(user_prompt)
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})

            response = get_chatbot_response(user_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)
    else:
        st.write("**Please enter your OpenAI API key to use the chatbot.**")
        api_key = st.text_input("OpenAI API Key", type="password")

        if st.button("Save API Key"):
            if api_key:
                save_api_key(api_key)
                st.success("API key saved successfully.")
                st.experimental_rerun()
            else:
                st.error("Please enter a valid API key.")
with open('styles.css') as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    