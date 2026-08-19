# 🎓 Student Record Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers natural-language
questions about student records. It combines a MySQL database, a Chroma
vector store, HuggingFace embeddings, and the Groq API for fast LLM
inference — all wrapped in a Streamlit chat interface.

> Final Year Project (FYP), [Your University Name] — [Year]

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![uv](https://img.shields.io/badge/dependency%20manager-uv-purple)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Natural-language student lookup** — e.g. *"What is Alice Smith's discipline?"*, *"Is Bob Johnson's fee paid?"*
- **RAG pipeline** — retrieves relevant records from a vector store before asking the LLM, instead of hoping the model already knows the answer
- **MySQL integration** — pulls live data from general, scholarship, and fee-submission tables
- **Groq-powered inference** — fast responses via Groq's hosted LLMs
- **Streamlit chat UI** — simple web interface with persistent chat history per session
- **General Q&A fallback** — answers questions that aren't about a specific student

## 📁 Project Structure

```
student-record-chatbot/
├── app.py                   # Streamlit entry point (streamlit run app.py)
├── src/
│   └── chatbot/
│       ├── config.py        # Environment variable loading & validation
│       ├── database.py      # MySQL connection & data fetching
│       ├── llm_client.py    # Groq API client
│       └── rag_pipeline.py  # Vector store setup, retrieval, prompting
├── data/
│   └── seed.sql             # Sample schema + synthetic data for local dev
├── tests/
│   └── test_rag_pipeline.py # Unit tests for query parsing
├── .env.example              # Template for required environment variables
├── pyproject.toml            # Dependencies (managed with uv)
└── README.md
```

## 🛠️ Setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — fast Python package/dependency manager
- A running MySQL server
- A [Groq API key](https://console.groq.com)

### 1. Clone and install dependencies

```bash
git clone https://github.com/<your-username>/student-record-chatbot.git
cd student-record-chatbot
uv sync
```

`uv sync` creates a virtual environment and installs everything pinned in
`pyproject.toml` / `uv.lock`. No manual `venv` or `pip install` steps needed.

### 2. Set up the database

Create the database, then load the sample schema and data:

```bash
mysql -u root -p -e "CREATE DATABASE project_data;"
mysql -u root -p project_data < data/seed.sql
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` and fill in your `GROQ_API_KEY` and MySQL credentials.

### 4. Run it

Streamlit web app:

```bash
uv run streamlit run app.py
```

Or the console version, useful for quick debugging without a browser:

```bash
uv run python -m chatbot.rag_pipeline
```

### Running tests

```bash
uv run pytest
```

## 💬 Example Queries

- "What is Alice Smith's discipline?"
- "Tell me about Charlie Brown's fee status."
- "Is Diana Prince enrolled in any scholarship?"
- "Hello, what can you do?"

## 🧱 Tech Stack

| Layer | Tool |
|---|---|
| LLM inference | [Groq API](https://groq.com) |
| Orchestration | [LangChain](https://www.langchain.com) |
| Embeddings | `sentence-transformers/all-mpnet-base-v2` (HuggingFace) |
| Vector store | [ChromaDB](https://www.trychroma.com) |
| Database | MySQL |
| UI | [Streamlit](https://streamlit.io) |
| Dependency management | [uv](https://docs.astral.sh/uv/) |

## 📝 Notes on the LLM model

Groq periodically retires older models. This project defaults to
`openai/gpt-oss-120b` via the `GROQ_MODEL` environment variable. If you hit a
`model_decommissioned` error, check [Groq's models page](https://console.groq.com/docs/models)
and set `GROQ_MODEL` in your `.env` to whatever's current — no code changes
needed.

## 🗺️ Roadmap / Future Improvements

- [ ] Join student records on a stable student ID instead of name (avoids collisions for duplicate names)
- [ ] Add authentication so only authorized staff can query records
- [ ] Support multi-turn follow-up questions ("what about his fee status?") using conversation context
- [ ] Add pagination / summarization for students with large scholarship/fee histories
- [ ] Deploy a live demo (Streamlit Community Cloud)
- [ ] Add CI (GitHub Actions) to run tests on every push

## 👥 Team

This was built as a 3-person Final Year Project team effort.

- [Your Name] — [your contribution, e.g. "database design & testing"]
- [Teammate 2] — [contribution]
- [Teammate 3] — [contribution]

## 📄 License

MIT — see [LICENSE](LICENSE).
