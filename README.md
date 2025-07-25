Student Record Chatbot
This project implements an intelligent chatbot designed to answer questions about student records. It utilizes a Retrieval-Augmented Generation (RAG) architecture, integrating with a MySQL database to fetch student-specific information, using Langchain for vector database management, and leveraging the Groq API for powerful language model inference. The chatbot provides an interactive user experience through a Streamlit web interface.

🚀 Features
Intelligent Student Information Retrieval: Ask natural language questions about specific students (e.g., "What is Alice Smith's discipline?", "Tell me about Bob Johnson's scholarship status.").

Retrieval-Augmented Generation (RAG): Combines a vector database with a large language model (LLM) to provide accurate and contextually relevant answers based on retrieved student data.

MySQL Database Integration: Seamlessly connects to a MySQL database to access student general data, scholarship information, and fee submission records.

HuggingFace Embeddings: Utilizes the sentence-transformers/all-mpnet-base-v2 model for generating high-quality text embeddings.

ChromaDB Vector Store: Efficiently stores and retrieves relevant student document chunks, enabling quick context lookup for the LLM.

Groq API Integration: Leverages the llama3-70b-8192 model via the Groq API for fast and intelligent text generation, ensuring quick response times.

Streamlit Web Interface: Offers a user-friendly and interactive chat interface, making the chatbot accessible and easy to use.

General Question Answering: Capable of handling general queries even when no specific student name is detected in the input.

📁 Project Structure
The project is organized into several modular Python files:

config.py: Manages environment variables crucial for API keys (Groq) and MySQL database connection details (host, user, password, database name).

database_handler.py: Contains functions to establish a connection to the MySQL database and to fetch and combine student data from student_general_data, student_scholarship, and student_fee_submission tables.

query_handler.py: Encapsulates the logic for making API calls to the Groq service, sending prompts, and receiving LLM-generated responses.

main.py: The core backend logic. It handles the setup of the vector database, extracts student names from user queries, constructs context-rich prompts using retrieved data, and orchestrates the interaction between the database, vector store, and LLM. This file can also be run as a standalone console application for testing.

app.py: The Streamlit application file that builds the graphical user interface for the chatbot, manages chat history, and integrates all backend functionalities for a seamless web experience.

🛠️ Setup and Installation
Follow these steps to get the Student Record Chatbot up and running on your local machine.

Prerequisites
Python 3.8 or higher

MySQL Database Server

1. Clone the Repository
First, clone the project repository to your local machine:

git clone https://github.com/Mawan-Khan/student-record-chatbot.git
cd student-record-chatbot

2. Create a Virtual Environment (Recommended)
It's good practice to use a virtual environment to manage project dependencies:

python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`

3. Install Dependencies
Install all the necessary Python packages using pip. If you don't have a requirements.txt file, you can create one by listing the following packages:

pip install python-dotenv mysql-connector-python langchain langchain-community chromadb sentence-transformers requests streamlit

Or, if you prefer to generate requirements.txt:

# After installing all packages manually, run:
pip freeze > requirements.txt
# Then, for future setups, you can just run:
# pip install -r requirements.txt

4. MySQL Database Setup
Connect to your MySQL server (e.g., using MySQL Workbench, command line, or phpMyAdmin).

Create a new database named project_data:

CREATE DATABASE project_data;
USE project_data;

Create the necessary tables and insert some sample student data. These tables are student_general_data, student_scholarship, and student_fee_submission.

-- Table for general student information
CREATE TABLE student_general_data (
    roll_number VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    discipline VARCHAR(100)
);

-- Table for student scholarship information
CREATE TABLE student_scholarship (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scholarship_name VARCHAR(100),
    enrollment_status VARCHAR(50)
);

-- Table for student fee submission status
CREATE TABLE student_fee_submission (
    registration_number VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    fee_status VARCHAR(50)
);

-- Insert Sample Data into student_general_data
INSERT INTO student_general_data (roll_number, name, discipline) VALUES
('2023-CS-001', 'Alice Smith', 'Computer Science'),
('2023-EE-005', 'Bob Johnson', 'Electrical Engineering'),
('2023-ME-010', 'Charlie Brown', 'Mechanical Engineering'),
('2023-CS-002', 'Diana Prince', 'Computer Science');

-- Insert Sample Data into student_scholarship
INSERT INTO student_scholarship (name, scholarship_name, enrollment_status) VALUES
('Alice Smith', 'Merit Scholarship', 'Enrolled'),
('Bob Johnson', 'Need-Based Grant', 'Pending'),
('Diana Prince', 'Athletic Scholarship', 'Enrolled');

-- Insert Sample Data into student_fee_submission
INSERT INTO student_fee_submission (registration_number, name, fee_status) VALUES
('REG-CS-001', 'Alice Smith', 'Paid'),
('REG-EE-005', 'Bob Johnson', 'Pending'),
('REG-ME-010', 'Charlie Brown', 'Paid'),
('REG-CS-002', 'Diana Prince', 'Overdue');

5. Environment Variables Configuration
Create a file named .env in the root directory of your project (the same directory as config.py) and add the following variables. Replace the placeholder values with your actual credentials.

GROQ_API_KEY="YOUR_GROQ_API_KEY"
DB_HOST="localhost"
DB_USER="root" # Your MySQL username
DB_PASSWORD="YOUR_MYSQL_PASSWORD" # The password for your MySQL user
DB_NAME="project_data"

GROQ_API_KEY: Obtain your API key from the Groq Console.

DB_HOST: The hostname of your MySQL database (e.g., localhost).

DB_USER: Your MySQL username (e.g., root).

DB_PASSWORD: The password associated with your MySQL user.

DB_NAME: The name of the database you created (e.g., project_data).

🚀 Running the Chatbot
Once all dependencies are installed and the database and environment variables are configured, you can launch the Streamlit application:

streamlit run app.py

This command will start the Streamlit server and open the chatbot interface in your default web browser.

💬 How to Use
Interact with the chatbot by typing your questions in the input field:

To ask about a specific student:

"What is Alice Smith's discipline?"

"Tell me about Charlie Brown's fee status."

"Is Diana Prince enrolled in any scholarship?"

"What are the details for Bob Johnson?"

To ask general questions:

"Hello!"

"What can you do?"

"Who are you?"

📚 Technologies Used
Python: The primary programming language.

Langchain: A framework for developing applications powered by language models.

HuggingFace Embeddings: Specifically sentence-transformers/all-mpnet-base-v2 for generating vector embeddings of text.

ChromaDB: A lightweight, open-source vector database used for efficient similarity search.

Groq API: Provides high-performance inference for large language models.

MySQL: A relational database management system used to store student records.

Streamlit: An open-source app framework for machine learning and data science teams to create beautiful, custom web apps.

python-dotenv: For loading environment variables from a .env file.

mysql-connector-python: The official MySQL driver for Python.

requests: A popular HTTP library for making API calls.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

📄 License
This project is open-source and distributed under the MIT License. See the LICENSE file (if present) for more details.
