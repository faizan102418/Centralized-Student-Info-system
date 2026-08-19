"""Core RAG pipeline: builds the vector store and answers student queries."""

import re
from pathlib import Path

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from chatbot.database import fetch_student_data_from_db
from chatbot.llm_client import query_groq_api

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# Where the combined text dump is cached for debugging. Relative to the
# project root so it works on any machine, not just the original author's.
DEBUG_DUMP_PATH = Path(__file__).resolve().parents[2] / "data" / "combined_student_records_from_db.txt"

NAME_PATTERN = re.compile(
    r"(?:student|for|of|about|details for|record of|show me|what is|tell me about)\s+"
    r"([A-Za-z][A-Za-z\s'-]*?)(?:'s\b|[?.,]|$)",
    re.IGNORECASE,
)


def setup_vector_db() -> Chroma:
    """Fetch all student data from MySQL and build an in-memory Chroma vector store."""
    combined_text = fetch_student_data_from_db()
    if not combined_text:
        raise ValueError(
            "No data fetched from the database to create a vector store. "
            "Make sure your database has data (see data/seed.sql)."
        )

    # Best-effort debug dump; never let this crash the app (e.g. read-only
    # deployments like Streamlit Community Cloud).
    try:
        DEBUG_DUMP_PATH.parent.mkdir(parents=True, exist_ok=True)
        DEBUG_DUMP_PATH.write_text(combined_text, encoding="utf-8")
    except OSError:
        pass

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(combined_text)
    if not chunks:
        raise ValueError("Text splitting produced no chunks from the database data.")

    documents = [Document(page_content=chunk) for chunk in chunks]
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma.from_documents(documents, embeddings)


def get_student_record_prompt(vectorstore: Chroma, student_name: str, user_question: str) -> str:
    """Retrieve relevant chunks for a student and build a grounded prompt."""
    retriever = vectorstore.as_retriever()
    relevant_docs = retriever.invoke(f"Information about {student_name}. {user_question}")

    if not relevant_docs:
        return ""

    retrieved_text = "\n\n".join(doc.page_content for doc in relevant_docs)
    return (
        f"Given the following extracted student records:\n{retrieved_text}\n\n"
        f'Answer the user\'s question about {student_name}: "{user_question}".\n'
        "Be concise and focus only on the information provided in the extracted "
        "records. If some details are not available, state that."
    )


def extract_student_name(query: str) -> str | None:
    """
    Best-effort, regex-based extraction of a student name from a free-text
    query. This is a heuristic, not real NLP/NER, so unusual phrasing can
    still confuse it — see README roadmap for a planned upgrade.
    """
    match = NAME_PATTERN.search(query)
    if not match:
        return None
    return " ".join(match.group(1).strip().split()).title()


def answer_question(vectorstore: Chroma, user_input: str) -> str:
    """Route a user question to a student-specific or general answer."""
    student_name = extract_student_name(user_input)
    if not student_name:
        return query_groq_api(user_input)

    prompt = get_student_record_prompt(vectorstore, student_name, user_input)
    if not prompt:
        return query_groq_api(user_input)

    return query_groq_api(prompt)


def run_console() -> None:
    """Interactive console loop for local testing without Streamlit."""
    vectorstore = setup_vector_db()
    print("Welcome to the Student Record Chatbot!")
    print("Ask me about a student by name (e.g., 'What is Alice Smith's discipline?').")
    print("You can also ask general questions. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit", "bye", "stop"}:
            print("Goodbye!")
            break
        print("Bot:", answer_question(vectorstore, user_input))


if __name__ == "__main__":
    run_console()
