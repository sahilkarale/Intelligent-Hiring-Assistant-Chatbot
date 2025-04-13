import os
import json
import streamlit as st
from display_it import display_chat
from message_handler import get_error_message,generate_field_prompt,analyze_sentiment,validate_with_llm
from validate import *

INFO_FIELDS = [
    ('Full Name', "text", None),
    ("Email", "text", is_valid_email),
    ("Phone", "text", is_valid_phone),
    ("Position", "text", None),
    ("Experience", "text", is_valid_experience),
    ('Tech Stack', "text", None),
    ('Location', "text", None)
]


data_file = "candidate_data.json"
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump([], f)

def save_candidate_data(candidate_info):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        data.append(candidate_info)
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving candidate data: {str(e)}")
        

def collect_candidate_info():
    if st.session_state.info_stage == 0:
        greeting = "👋 Hello! I'm **TalentScout**, your AI hiring assistant. Let's get started!"
        if not any(msg['content'] == greeting for msg in st.session_state.conversation):
            st.session_state.conversation.append({'role': 'assistant', 'content': greeting})
        st.session_state.info_stage = 1
        st.rerun()

    if st.session_state.info_stage == 1:
        display_chat()

        if st.session_state.current_field < len(INFO_FIELDS):
            field_name, field_type, validator = INFO_FIELDS[st.session_state.current_field]

            if not st.session_state.current_prompt_sent:
                prompt = generate_field_prompt(field_name)
                st.session_state.conversation.append({'role': 'assistant', 'content': prompt})
                st.session_state.current_prompt_sent = True
                st.rerun()

            user_input = st.chat_input("Your response...")
            if user_input:
                # Analyze sentiment and update session state
                sentiment = analyze_sentiment(user_input)
                st.session_state.last_sentiment = sentiment
                
                st.session_state.conversation.append({
                    'role': 'user',
                    'content': user_input,
                    'sentiment': sentiment
                })
                valid, validation_msg = True, ""

                if validator and not validator(user_input.strip()):
                    valid = False
                    validation_msg = f"❌ {get_error_message(field_name)}"
                else:
                    is_valid, llm_msg = validate_with_llm(field_name, user_input.strip())
                    if not is_valid:
                        valid = False
                        validation_msg = f"⚠️ {llm_msg}"

                if valid:
                    st.session_state.candidate_info[field_name] = user_input.strip()
                    st.session_state.current_field += 1
                    st.session_state.current_prompt_sent = False
                    if st.session_state.current_field >= len(INFO_FIELDS):
                        st.session_state.info_stage = 2
                        save_candidate_data(st.session_state.candidate_info)
                else:
                    st.session_state.conversation.append({'role': 'assistant', 'content': validation_msg})

                st.rerun()

        else:
            st.session_state.info_stage = 2
            st.rerun()

    elif st.session_state.info_stage == 2:
        display_chat()
        st.success("✅ All information collected successfully!")

        st.markdown("### Please confirm your details:")
        for field, value in st.session_state.candidate_info.items():
            st.markdown(f"**{field}:** {value}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm and Start Interview", use_container_width=True):
                st.session_state.interview_state = "in_progress"
                st.rerun()
        with col2:
            if st.button("🔄 Edit Information", use_container_width=True):
                st.session_state.update({
                    'info_stage': 0,
                    'current_field': 0,
                    'current_prompt_sent': False,
                    'conversation': [],
                    'candidate_info': {k: None for k in st.session_state.candidate_info}
                })
                st.rerun()