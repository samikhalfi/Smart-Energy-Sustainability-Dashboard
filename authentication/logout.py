import streamlit as st

def logout():

    st.markdown("""
    <div style="text-align: center;">
        <h3>It looks like you're ready to say goodbye! 😢</h3>
        <p>Click the button below to log out. If you decide to come back, I'll be here waiting with more fun and useful insights!</p>
        <div style="margin-top: 20px;">
            <img src="https://img.icons8.com/ios-filled/30/000000/logout-rounded.png" alt="Logout Icon"/>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Logout", key="logout_button", use_container_width=True):
        st.session_state.clear() 
        st.success("You have been logged out. See you next time! 👋")
        st.experimental_rerun()
        
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <h4 style="font-size: 20px;">Connect with Me 🌐</h4>
        <div style="display: flex; justify-content: center; gap: 15px;">
            <a href="https://www.linkedin.com/in/sami-khalfi-355098290/" target="_blank">
                <img src="https://img.icons8.com/ios-filled/30/000000/linkedin.png" alt="LinkedIn Icon"/>
                <br>LinkedIn
            </a>
            <a href="https://github.com/samikhalfi" target="_blank">
                <img src="https://img.icons8.com/ios-filled/30/000000/github.png" alt="GitHub Icon"/>
                <br>GitHub
            </a>
        </div>
        <div style="margin-top: 20px;">
            <img src="https://img.icons8.com/ios-filled/30/000000/happy.png" alt="Happy Icon"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

with open('styles.css') as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
