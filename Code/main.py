# main.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from database_handler import fetch_student_data_from_db
from query_handler import query_groq_api
import re

def setup_vector_db():
    """
    Sets up the vector database from all fetched database records at startup.
    """
    
    combined_text = fetch_student_data_from_db() 

    if not combined_text:
        # This is a critical error, so it's good to keep this message
        raise ValueError("No data fetched from the database to create vectorstore. Please ensure your database has data.")

    # You can optionally save the combined_text to a file for debugging
    combined_doc_path = "D:/DB project/Temp/combined_student_records_from_db.txt"
    with open(combined_doc_path, "w", encoding="utf-8") as f:
        f.write(combined_text)
    print(f"✅ Combined database text for embeddings saved at: {combined_doc_path}")

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(combined_text)
    if not texts:
        raise ValueError("Text splitting failed—no chunks generated from database data.")
    documents = [Document(page_content=t) for t in texts]
    if not documents:
        raise ValueError("No documents were created for embeddings. Check text splitting from database data.")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    print(f"Total documents processed from database for RAG: {len(documents)}")
    vectorstore = Chroma.from_documents(documents, embeddings)
    return vectorstore

def get_student_record_prompt(vectorstore, student_name, user_question):
    """
    Retrieves the student record from the vector database and formats the prompt.
    Now uses the full user_question for retrieval to provide better context.
    """
    retriever = vectorstore.as_retriever()
    
    # Use the student_name and the original user_question to find relevant documents
    relevant_docs = retriever.get_relevant_documents(f"Information about {student_name}. {user_question}")
    
    if not relevant_docs:
        # If no relevant documents, return an empty string to indicate no specific context was found
        return "" 

    retrieved_text = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    combined_prompt = f"""Given the following extracted student records:
{retrieved_text}

Answer the user's question about {student_name}: "{user_question}".
Be concise and focus only on the information provided in the extracted records. If some details are not available, state that.
"""
    return combined_prompt

def extract_student_name(query):
    """
    Extracts the student name from the user query using regular expressions.
    Focuses solely on extracting the name.
    """
    # Pattern to capture words/spaces for name after keywords like "student", "about", "for"
    name_pattern = r"(?:student|for|of|about|details for|record of|show me|what is|tell me about)\s+([A-Za-z\s'-]+)"
    name_match = re.search(name_pattern, query, re.IGNORECASE)
    
    student_name = None
    if name_match:
        # Clean up the extracted name: remove leading/trailing spaces, extra internal spaces, title case
        student_name = " ".join(name_match.group(1).strip().split()).title()
    
    return student_name

def main():
    """
    Main function to run the interactive student record retrieval chat.
    """
    
    vectorstore = setup_vector_db() # Setup vector DB once at the beginning
    print("Welcome to the Student Record Chatbot!")
    print("Ask me about a student by name (e.g., 'What is Alice Smith's discipline?').")
    print("You can also ask general questions.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye", "stop"]:
            print("Goodbye!")
            break
        
        student_name = extract_student_name(user_input)
        
        if student_name:
            # We still print this to indicate the *intent* to search for a student
            print(f"Searching for information about student: {student_name}...")
            
            # Generate prompt for student-specific query
            prompt = get_student_record_prompt(vectorstore, student_name, user_input)
            
            if not prompt: 
                # If no relevant docs were found, just pass the original user_input to LLM.
                # The LLM will then try to answer generally or state it has no info based on its own knowledge.
                response = query_groq_api(user_input)
                print("Bot:", response)
                continue # Go to next loop iteration

            response = query_groq_api(prompt)
            print("Bot:", response)
        else:
            # If no student name is detected, directly pass the raw user input for general questions.
            # Removed the explicit print statement for a smoother transition.
            response = query_groq_api(user_input)
            print("Bot:", response)

if __name__ == "__main__":
    main()