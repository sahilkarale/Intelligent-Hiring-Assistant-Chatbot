import streamlit as st


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