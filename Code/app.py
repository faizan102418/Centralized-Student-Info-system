# app.py
import streamlit as st
import sys
import os

# Add the project directory to the Python path to allow imports of your modules
# This assumes app.py is in the same directory as main.py, database_handler.py, etc.
sys.path.append(os.path.dirname(__file__))

# Import functions from your existing files
from main import setup_vector_db, extract_student_name, get_student_record_prompt
from query_handler import query_groq_api


# --- Streamlit UI Setup ---
st.set_page_config(page_title="Student Record Chatbot")
st.title("👨‍🎓 Student Record Chatbot")
st.markdown("Ask me about a student by name (e.g., 'What is Alice Smith's discipline?'). You can also ask general questions.")

# --- Initialize Vector Store (Cached to run only once) ---
@st.cache_resource
def load_vector_db():
    """Caches the vector database loading to run only once."""
    try:
        with st.spinner("Loading student data and setting up knowledge base..."):
            vectorstore = setup_vector_db()
        st.success("Knowledge base loaded successfully!")
        return vectorstore
    except Exception as e:
        st.error(f"Failed to load knowledge base: {e}")
        st.stop() # Stop the app if DB loading fails

vectorstore = load_vector_db()

# --- Chat Interface ---

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            student_name = extract_student_name(prompt)
            response_content = ""

            if student_name:
                # Try to get student-specific information
                # print(f"Searching for information about student: {student_name}...") # Streamlit prints to console
                specific_prompt = get_student_record_prompt(vectorstore, student_name, prompt)
                
                if specific_prompt:
                    # If specific student data was found and context generated
                    response_content = query_groq_api(specific_prompt)
                else:
                    # If student name extracted but no relevant docs found for specific context,
                    # treat as a general question. LLM can respond "I don't have info on that"
                    # if it thinks it's a student question but has no context.
                    response_content = query_groq_api(prompt)
            else:
                # No student name detected, treat as a general question
                response_content = query_groq_api(prompt)

            st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})