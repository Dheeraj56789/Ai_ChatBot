import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Initialize Gemini model
chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Heart Rate Monitor Assistant", layout="wide")

st.title("💓 AI Heart Rate Monitor Assistant")
st.subheader("Analyzes heart rate data and provides insights")
st.subheader("Developed By - 12313013 DHEERAJ SINGH")

# List of heart-related keywords
heart_keywords = [
    "hi","hello","heart", "heartbeat", "heart rate", "pulse", "bpm", "cardiac",
    "tachycardia", "bradycardia", "arrhythmia", "ECG", "electrocardiogram",
    "blood pressure", "chest pain", "palpitation", "irregular heartbeat"
]

# Check if prompt is heart-related
def is_heart_related(prompt):
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in heart_keywords)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Enter heart rate readings or symptoms...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    if is_heart_related(user_input):
        # Generate response only if heart-related
        response = chat_model.invoke(user_input) 
        response_text = response.content if hasattr(response, "content") else str(response)
    else:
        # Custom message for non-heart-related questions
        response_text = "⚠️ I'm here to help only with heart rate and cardiac-related questions. Please ask something relevant."

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response_text)
