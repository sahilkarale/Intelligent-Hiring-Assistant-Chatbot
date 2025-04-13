import streamlit as st 
from langchain_core.messages import HumanMessage, SystemMessage
from config import get_llm

get_llm =  get_llm()
def analyze_sentiment(text):
    """Analyze text sentiment using LLM."""
    messages = [
        SystemMessage(content="Analyze the sentiment of the following text. Respond with exactly one word: 'positive', 'neutral', or 'negative'."),
        HumanMessage(content=text)
    ]
    try:
        response = get_llm.invoke(messages).content.strip().lower()
        if 'positive' in response:
            return 'positive'
        elif 'negative' in response:
            return 'negative'
        return 'neutral'
    except Exception as e:
        st.error(f"Sentiment analysis error: {e}")
        return 'neutral'