# ========== 1. IMPORTS AND SETUP ==========

import streamlit as st
import re
import nltk
from nltk.tokenize import word_tokenize
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from nltk.tokenize import word_tokenize
from langchain_groq import ChatGroq
import json
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

nltk.download('punkt')

llm = ChatGroq(model="Llama3-8b-8192", groq_api_key=GROQ_API_KEY, temperature=0.7)

# ========== 2. SESSION STATE INITIALIZATION ==========

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

# ========== 3. VALIDATION FUNCTIONS ==========

def is_valid_experience(input_text):
    pattern = r'^\s*\d+(\.\d+)?\s*(years?|months?)\s*$'
    return re.match(pattern, input_text.strip(), re.IGNORECASE) is not None

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone) is not None

def validate_with_llm(field_name, value):
    validation_prompts = {
        'Email': f"Verify if this email could belong to a real person: {value}. Consider domain validity and common patterns. Respond 'valid' or 'invalid' with a brief reason.",
        'Phone': f"Check if this phone number could be valid: {value}. Consider country codes and formatting. Respond 'valid' or 'invalid' with a reason.",
        'Experience':f"Check if the following clearly expresses professional experience in terms of duration in years only, like '2 years' or '5+ years'. Respond 'valid' or 'invalid' with a brief reason.",
        'Tech Stack': f"Verify if these technologies could form a coherent skillset: {value}. Respond 'coherent' or 'incoherent' with a reason.",
        'Position': f"Is '{value}' a recognized job title in the tech industry? Respond 'valid' or 'invalid' with a reason."
    }

    if field_name not in validation_prompts:
        return True, ""

    messages = [
        SystemMessage(content="You're an HR validation system. Analyze critically but professionally."),
        HumanMessage(content=validation_prompts[field_name])
    ]

    try:
        response = llm.invoke(messages).content.strip().lower()
        if 'invalid' in response or 'incoherent' in response:
            reason = response.split(':', 1)[-1].strip() if ':' in response else 'Reason not provided.'
            return False, f"This {field_name.lower()} seems unusual: {reason}"
        return True, ""
    except Exception as e:
        st.error(f"Validation error: {e}")
        return True, ""

def get_error_message(field_name):
    error_messages = {
        'Email': "Please enter a valid email address (e.g., example@domain.com)",
        'Phone': "Please enter a valid phone number (e.g., +1234567890)",
        'Experience': "Please enter a valid number of years (0-50)",
        'default': "Invalid input, please try again."
    }
    return error_messages.get(field_name, error_messages['default'])
# ========== 4. DATA MANAGEMENT ==========

def save_candidate_data(candidate_info):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        data.append(candidate_info)
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving candidate data: {str(e)}")
        
# ========== 5. CHAT INTERFACE COMPONENTS ==========

def show_welcome_screen():
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 36px; color: #F1F1F1;'>🚀 Welcome to <span style="color:#4F8BF9;">TalentScout AI</span> Interview Station 🤖</h1>
        <p style='font-size: 18px; max-width: 800px; margin: 0 auto; color: #CCCCCC;'>
            <b>TalentScout</b> is your AI-powered interviewing assistant designed to conduct intelligent, responsive, and adaptive technical interviews tailored to your profile.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='max-width: 900px; margin: auto; font-size: 16px; padding: 15px 30px; background-color: #2D2D2D; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); color: #E0E0E0;'>
            <ul>
                <li>📝 <b>Initial Screening:</b> Provide your basic information and technical background</li>
                <li>🧠 <b>Technical Assessment:</b> Answer skill-specific questions across your tech stack</li>
                <li>🔄 <b>Interactive Dialogue:</b> Dynamic follow-up questions based on your responses</li>
                <li>📊 <b>Immediate Analysis:</b> Real-time evaluation of your technical proficiency</li>
            </ul>
            <p>
                Our AI system uses advanced natural language processing to:
                <ul>
                    <li>✅ Evaluate depth of technical knowledge</li>
                    <li>✅ Assess problem-solving approaches</li>
                    <li>✅ Analyze communication clarity</li>
                </ul>
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("🎯 Begin Interview Now", use_container_width=True):
            st.session_state['interview_state'] = "collecting_info"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def display_chat():
    st.markdown("""
    <style>
    .chat-bubble {
        padding: 1rem;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 80%;
        position: relative;
    }
    .assistant {
        background: #2e2e2e;
        margin-right: auto;
    }
    .user {
        background: #4F8BF9;
        color: white;
        margin-left: auto;
    }
    .sentiment-indicator {
        position: absolute;
        right: -30px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.conversation:
        bubble_class = "assistant" if msg['role'] == 'assistant' else "user"
        content = msg['content']
        
        if msg['role'] == 'user':
            sentiment = msg.get('sentiment', 'neutral')
            emoji_map = {
                'positive': '😊',
                'neutral': '😐',
                'negative': '😟'
            }
            sentiment_emoji = emoji_map.get(sentiment, '')
            content += f" <span class='sentiment-indicator'>{sentiment_emoji}</span>"
        
        st.markdown(f"<div class='chat-bubble {bubble_class}'>{content}</div>", 
                    unsafe_allow_html=True)

def show_progress():
    tech_stack = st.session_state.candidate_info['Tech Stack'].split(',')
    current_tech = tech_stack[st.session_state.tech_stack_index]
    progress = (st.session_state.tech_stack_index/len(tech_stack)) + (
        len(st.session_state.answers.get(current_tech,{}))/(3*len(tech_stack)))
    st.progress(min(progress, 1.0))
    st.caption(f"Progress: Technology {st.session_state.tech_stack_index+1} of {len(tech_stack)}")
    
def show_summary():
    if st.session_state.get('thank_you_shown', False):
        st.empty()
        
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h1 style='color: #4CAF50;'>🎉 Thank You! 🎉</h1>
            <p style='font-size: 20px; margin-top: 30px;'>
                We truly appreciate you taking the time to complete this interview process.
            </p>
            <div style='margin-top: 40px;'>
                <h3>Next Steps:</h3>
                <ul style='display: inline-block; text-align: left;'>
                    <li>Our team will review your application</li>
                    <li>You'll hear back within 3-5 business days</li>
                    <li>Possible follow-up interviews if needed</li>
                </ul>
            </div>
            <div style='margin-top: 50px;'>
                <p>For any questions, contact:</p>
                <p><strong>careers@yourcompany.com</strong></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("## 🎉 Interview Complete!")
    st.markdown("### 📋 Your Information")
    candidate = st.session_state['candidate_info']
    st.markdown(f"**👤 Name:** {candidate['Full Name']}")
    st.markdown(f"**💼 Position:** {candidate['Position']}")
    st.markdown(f"**📅 Experience:** {candidate['Experience']} years")

    st.markdown("### 📝 Your Answers")
    for tech, qa_pairs in st.session_state['answers'].items():
        st.markdown(f"#### {tech}")
        for question, answer in qa_pairs.items():
            st.markdown(f"**Q:** {question}")
            st.markdown(f"**A:** {answer}")
            st.markdown("---")

    st.markdown("## ❓ Any Final Questions?")
    st.markdown("If you have any additional enquiries about the position or next steps, please let us know below.")

    enquiry = st.text_area("Your enquiry:", key="enquiry_input", height=100)
    col_spacer_left, col1, col2, col_spacer_right = st.columns([3, 2, 2, 3])

    with col1:
        if st.button("✉️ Submit Enquiry", use_container_width=True):
            if enquiry.strip():
                st.session_state['submitted_enquiry'] = enquiry
                st.session_state['thank_you_shown'] = True
                st.rerun()
            else:
                st.warning("Please enter your enquiry before submitting.")

    with col2:
        if st.button("🚀 No Questions", use_container_width=True):
            st.session_state['submitted_enquiry'] = None
            st.session_state['thank_you_shown'] = True
            st.rerun()
# ========== 6. INFORMATION COLLECTION ==========
 
INFO_FIELDS = [
    ('Full Name', "text", None),
    ("Email", "text", is_valid_email),
    ("Phone", "text", is_valid_phone),
    ("Position", "text", None),
    ("Experience", "text", is_valid_experience),
    ('Tech Stack', "text", None),
    ('Location', "text", None)
]

def generate_field_prompt(field_name):
    messages = [
        SystemMessage(content="You're an HR assistant collecting candidate information. Be friendly and professional."),
        HumanMessage(content=f"Generate a one-sentence prompt to ask for {field_name}:")
    ]
    response = llm.invoke(messages)
    return response.content.strip()

data_file = "candidate_data.json"
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump([], f)
        

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

# ========== 7. INTERVIEW LOGIC ==========

def generate_first_question(tech):
    prompt = f"""
    Generate an opening technical interview question about {tech} for a candidate with {
        st.session_state.candidate_info['Experience']} years of experience.
    Focus on core concepts. Return only the question.
    """
    messages = [
        SystemMessage(content="You are a technical interviewer."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content.strip()

def generate_followup_question(tech, prev_question, prev_answer):
    prompt = f"""
    Based on this answer to '{prev_question}': {prev_answer}
    Generate a follow-up question about {tech}. Focus on depth and technical accuracy.
    Return only the question.
    """
    messages = [
        SystemMessage(content="You are a technical interviewer."),
        HumanMessage(content=prompt)
    ]
    return llm.invoke(messages).content.strip()

def handle_previous_question():
    if len(st.session_state.question_history) > 1:
        st.session_state.question_history.pop()
        prev_tech, prev_question = st.session_state.question_history[-1]
        st.session_state.current_question = prev_question
        st.session_state.tech_stack_index = st.session_state.candidate_info['Tech Stack'].split(',').index(prev_tech)
    st.rerun()

def handle_next_question(current_tech, answer):
    # Analyze sentiment for interview answers
    sentiment = analyze_sentiment(answer)
    st.session_state.last_sentiment = sentiment
    
    st.session_state.answers[current_tech][st.session_state.current_question] = answer
    tech_stack = st.session_state.candidate_info['Tech Stack'].split(',')
    
    if len(st.session_state.answers[current_tech]) >= 3:
        if st.session_state.tech_stack_index < len(tech_stack) - 1:
            st.session_state.tech_stack_index += 1
            st.session_state.current_question = None
        else:
            st.session_state.interview_state = "completed"
    else:
        new_question = generate_followup_question(
            current_tech,
            st.session_state.current_question,
            answer
        )
        st.session_state.current_question = new_question
        st.session_state.question_history.append((current_tech, new_question))
    st.rerun()

def conduct_interview():
    tech_stack = [t.strip() for t in st.session_state.candidate_info['Tech Stack'].split(',')]
    current_tech = tech_stack[st.session_state.tech_stack_index]
    
    st.markdown(f"## 🔍 Technical Interview: {current_tech}")
    st.markdown(f"**Experience Level:** {st.session_state.candidate_info['Experience']} years")
    
    if current_tech not in st.session_state.answers:
        st.session_state.answers[current_tech] = {}
        st.session_state.current_question = generate_first_question(current_tech)
        st.session_state.question_history.append((current_tech, st.session_state.current_question))
    
    st.markdown(f"### ❓ Question:")
    st.markdown(st.session_state.current_question)
    
    answer = st.text_area("Your answer:", key=f"answer_{len(st.session_state.answers[current_tech])}", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏮ Previous",use_container_width=True):
            handle_previous_question()
    with col2:
        if st.button("⏭ Next",use_container_width=True):
            handle_next_question(current_tech, answer)
    
    show_progress()

# ========== 8. SENTIMENT ANALYSIS ==========

def analyze_sentiment(text):
    """Analyze text sentiment using LLM."""
    messages = [
        SystemMessage(content="Analyze the sentiment of the following text. Respond with exactly one word: 'positive', 'neutral', or 'negative'."),
        HumanMessage(content=text)
    ]
    try:
        response = llm.invoke(messages).content.strip().lower()
        if 'positive' in response:
            return 'positive'
        elif 'negative' in response:
            return 'negative'
        return 'neutral'
    except Exception as e:
        st.error(f"Sentiment analysis error: {e}")
        return 'neutral'
    
def display_sentiment():
    sentiment = st.session_state.last_sentiment
    emoji_map = {
        'positive': ('😊', '#4CAF50'),
        'neutral': ('😐', '#FFC107'),
        'negative': ('😟', '#F44336')
    }
    emoji, color = emoji_map.get(sentiment, ('😐', '#FFC107'))
    
    st.sidebar.markdown(f"""
    <div style='padding: 20px; border-radius: 10px; background-color: {color}20; border-left: 5px solid {color};'>
        <h3 style='color: {color}; margin: 0;'>Current Sentiment</h3>
        <div style='font-size: 48px; text-align: center; margin: 20px 0;'>{emoji}</div>
        <p style='margin: 0; text-align: center; font-weight: bold; color: {color};'>
            {sentiment.capitalize()}
        </p>
    </div>
    """, unsafe_allow_html=True)







# ========== 9. MAIN APPLICATION FLOW ==========
 
def main():
    st.set_page_config(page_title="TalentScout AI Interview", page_icon="🤖", layout="wide")
    
    # Sidebar Elements
    st.sidebar.image("Logo.webp")
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