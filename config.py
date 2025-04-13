# config.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_llm():
    return ChatGroq(
        model="Llama3-8b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
