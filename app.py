# app.py
import streamlit as st
import nltk
from display_it import display_sentiment,show_summary,show_welcome_screen
from candidate_info import collect_candidate_info
from message_handler import conduct_interview


# Initialize session state and components
nltk.download('punkt')



if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'last_sentiment' not in st.session_state:
    st.session_state.last_sentiment = 'neutral'
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {
        'Full Name': None,
        'Email': None,
        'Phone': None,
        'Experience': None,
        'Position': None,
        'Location': None,
        'Tech Stack': None
    }
if 'info_stage' not in st.session_state:
    st.session_state.info_stage = 0
if 'current_field' not in st.session_state:
    st.session_state.current_field = 0
if 'current_prompt_sent' not in st.session_state:
    st.session_state.current_prompt_sent = False
if 'interview_state' not in st.session_state:
    st.session_state.interview_state = "not_started"
if 'tech_stack_index' not in st.session_state:
    st.session_state.tech_stack_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'question_history' not in st.session_state:
    st.session_state.question_history = []  

def main():
    st.set_page_config(page_title="TalentScout AI Interview", page_icon="🤖", layout="wide")
    
    # Sidebar Elements
    st.sidebar.image("Logo.jpeg")
    st.sidebar.markdown("---")
    
    # Real-time Sentiment Display
    display_sentiment()
    
    # Always-visible Reset Button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Interview", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    if st.session_state.interview_state == "not_started":
        show_welcome_screen()
    elif st.session_state.interview_state == "collecting_info":
        collect_candidate_info()
    elif st.session_state.interview_state == "in_progress":
        conduct_interview()
    elif st.session_state.interview_state == "completed":
        show_summary()


    
if __name__ == "__main__":
    main()
