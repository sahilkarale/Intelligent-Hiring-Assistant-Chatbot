# 🎯 TalentScout AI – Intelligent Hiring Assistant

TalentScout AI is a powerful, interactive, and modular hiring assistant powered by **LLaMA 3** via the **Groq API**, built using **LangChain** and **Streamlit**. It simulates the initial phase of a technical interview by gathering candidate information in a conversational manner, validating inputs using both regex and LLMs, and preparing the candidate profile for further analysis or question generation.

---

## 📌 Table of Contents

1. [Project Objectives](#-project-objectives)  
2. [Features](#-features-overview)  
3. [Tech Stack](#-tech-stack)  
4. [LLM Prompts & Usage](#-llm-prompts--conversations)  
5. [Setup Instructions](#-setup-instructions)  
6. [Sample Workflow](#-sample-use-case--flow)  
7. [Technical Interview Questions](#-technical-interview-questions)  
8. [Future Enhancements](#-future-enhancements)  
9. [Author](#-author)  
10. [Thanks](#-thanks)

---

## 🎯 Project Objectives

- 🤖 Simulate an intelligent AI-based interview assistant  
- 📋 Collect structured candidate data conversationally  
- 🧠 Use LLMs for prompt engineering, validation, and reasoning  
- 🔒 Ensure input validity and completeness  
- 💾 Store responses for analysis and next-step evaluation  

---

## 🧠 Features Overview

### ✅ Conversational Interface
- User-friendly interaction using Streamlit Chat
- Welcomes and guides the user step-by-step

### 📝 Candidate Information Collection
Captures:
- Full Name  
- Email ID  
- Phone Number  
- Location  
- Role Applied For  
- Primary Tech Stack  
- Years of Experience  

### 🔍 Smart Input Validation
- Regex-based validation for phone and email  
- LLM-based validation for ambiguous roles or stacks  

### 💬 LLM Integration
- Uses **LangChain** to send prompts to **LLaMA 3** via Groq API  
- Prompts tailored for:
  - Data collection
  - Validation
  - Clarification
  - User engagement  

### 🧪 Technical Interview Simulation (Phase 2)
- Based on user’s tech stack, the LLM generates custom technical questions
- Validates length, complexity, and variety of responses

### 📊 Token Analysis & Response Handling
- Ensures user provides substantial input (not just 1-2 words)
- LLM re-prompts user if message is too short or unclear

### 💾 Local Data Storage
- Stores collected information in a JSON file (`candidate_data.json`)

---

## 🛠️ Tech Stack

| Component     | Technology                  |
| ------------- | --------------------------- |
| UI Framework  | Streamlit                   |
| LLM Framework | LangChain                   |
| LLM           | Meta's LLaMA 3 via Groq API |
| Data Storage  | JSON                        |
| NLP Tools     | NLTK                        |
| Environment   | Python (.env, venv)         |

---

## 🧠 LLM Prompts & Conversations

The LLM (LLaMA 3) is used for multiple stages of the interaction:

### 1. Initial Greeting Prompt
```
You're a friendly AI recruiter. Start by greeting the candidate and introducing yourself. Then ask for their full name.
```

### 2. Role Verification Prompt
```
The user says they are applying for the role: '{{user_input}}'. Does this sound like a valid tech job role? If not, ask them to clarify.
```

### 3. Tech Stack Check
```
The user mentions their primary tech stack is '{{user_input}}'. List the known technologies from this stack. If ambiguous, ask for clarification.
```

### 4. Clarification Prompt for Short Inputs
```
The user responded: '{{user_input}}'. This seems too short or unclear. Politely ask them to elaborate more.
```

### 5. Candidate Summary (Planned for Phase 2)
```
Based on the inputs: Name, Role, Tech Stack, Experience – write a short summary of the candidate’s profile.
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sahilkarale/Intelligent-Hiring-Assistant-Chatbot.git
cd talentscout-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing:
```bash
pip install streamlit langchain langchain-groq python-dotenv nltk
```

### 4. Add Environment Variables
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Streamlit App
```bash
streamlit run app.py
```

## 🔄 Sample Use Case / Flow

```
AI: Hello! I’m TalentScout – your AI-based interview assistant 🤖  
AI: Let's start by getting your full name.  
User: Alex Morgan  
AI: Great Alex! Can you share your email?  
User: alex@domain.com  
AI: And your phone number?  
User: +1 234 567 8900  
AI: What role are you applying for?  
User: React Developer  
AI: Nice! What’s your primary tech stack?  
User: React, JavaScript, Node.js  
AI: How many years of experience do you have?  
User: 3 years  
AI: Awesome! Let me summarize this info...

Then, based on your stack, here are some questions:  
🧠 "What are the lifecycle methods in React?"  
⚙️ "Explain how `useEffect` works and when you'd use it."  
💡 "How does Node.js handle asynchronous operations?"  
```

---

## 🧪 Technical Interview Questions

This module uses LLaMA 3 to generate **context-aware technical questions** based on the user's tech stack. For example:

If a candidate mentions:
```
Stack: Python, Django, PostgreSQL
```
Then the LLM might ask:
- "What is the difference between Django ORM and raw SQL queries?"
- "How do migrations work in Django?"
- "How do you secure sensitive data in a Django application?"

Or for:
```
Stack: React, Node.js, MongoDB
```
It might ask:
- "What is the Virtual DOM in React?"
- "How do you handle authentication in a Node.js app?"
- "What is a NoSQL database and why use MongoDB?"

This enables **tailored technical screening** right after data collection.

---

## 📈 Future Enhancements

- 🧠 Resume Upload + Parsing using OCR + LLM  
- 🧑‍💻 Tech Stack-Based MCQ/Coding Questions  
- 🗂️ Candidate Profile Generator  
- 📊 Recruiter Analytics Dashboard  
- 🌐 Cloud DB Integration (MongoDB, Supabase, Firebase)  
- 🔒 Admin Login for Recruiters  

---

## 👨‍💻 Author

**Sahil Karale**  
Enthusiastic AI/ML Engineer   
🔗 [LinkedIn](https://www.linkedin.com/in/sahilkarale/)  
🐙 [GitHub](https://github.com/sahilkarale?tab=repositories)

---

## 🙏 Thanks

Huge thanks to the open-source community, [Meta AI](https://ai.meta.com/llama/), [Groq](https://groq.com/), [LangChain](https://www.langchain.com/), and the [Streamlit](https://streamlit.io/) team for enabling this project to come to life.

Also, thank you for checking out this project! ⭐ Feel free to fork, contribute, and share!
