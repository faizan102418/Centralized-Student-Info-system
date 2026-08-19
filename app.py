"""Streamlit UI for the Student Record Chatbot.

Run with: streamlit run app.py
"""

import sys
from pathlib import Path

# Make the src/ layout importable without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st

from chatbot.rag_pipeline import answer_question, setup_vector_db

st.set_page_config(page_title="Student Record Chatbot", page_icon="🎓")
st.title("🎓 Student Record Chatbot")
st.markdown(
    "Ask me about a student by name (e.g., *'What is Alice Smith's discipline?'*). "
    "You can also ask general questions."
)


@st.cache_resource
def load_vector_db():
    with st.spinner("Loading student data and setting up knowledge base..."):
        return setup_vector_db()


try:
    vectorstore = load_vector_db()
except Exception as exc:  # noqa: BLE001
    st.error(f"Failed to load knowledge base: {exc}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = answer_question(vectorstore, prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
