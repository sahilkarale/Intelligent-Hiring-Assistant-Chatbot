import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from sentiment import analyze_sentiment
from config import get_llm

get_llm = get_llm()

def generate_field_prompt(field_name):
    messages = [
        SystemMessage(content="You're an HR assistant collecting candidate information. Be friendly and professional."),
        HumanMessage(content=f"Generate a one-sentence prompt to ask for {field_name}:")
    ]
    response = get_llm.invoke(messages)
    return response.content.strip()

def get_error_message(field_name):
    error_messages = {
        'Email': "Please enter a valid email address (e.g., example@domain.com)",
        'Phone': "Please enter a valid phone number (e.g., +1234567890)",
        'Experience': "Please enter a valid number of years (0-50)",
        'default': "Invalid input, please try again."
    }
    return error_messages.get(field_name, error_messages['default'])


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
        response = get_llm.invoke(messages).content.strip().lower()
        if 'invalid' in response or 'incoherent' in response:
            reason = response.split(':', 1)[-1].strip() if ':' in response else 'Reason not provided.'
            return False, f"This {field_name.lower()} seems unusual: {reason}"
        return True, ""
    except Exception as e:
        st.error(f"Validation error: {e}")
        return True, ""

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
    return get_llm.invoke(messages).content.strip()

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
    return get_llm.invoke(messages).content.strip()


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
    
    
def show_progress():
    tech_stack = st.session_state.candidate_info['Tech Stack'].split(',')
    current_tech = tech_stack[st.session_state.tech_stack_index]
    progress = (st.session_state.tech_stack_index/len(tech_stack)) + (
        len(st.session_state.answers.get(current_tech,{}))/(3*len(tech_stack)))
    st.progress(min(progress, 1.0))
    st.caption(f"Progress: Technology {st.session_state.tech_stack_index+1} of {len(tech_stack)}")