# Personal Codex Agent

## Overview

**Personal Codex Agent** is an AI-powered assistant designed to help users interact with and manage their personal knowledge base. It leverages advanced language models and modern Python libraries to provide intelligent search, summarization, and automation capabilities for your documents and notes.

## Features

- **Natural Language Querying:** Ask questions in plain English and get relevant answers from your knowledge base.
- **Document Ingestion:** Easily add and organize documents, notes, and other resources.
- **Summarization:** Generate concise summaries of lengthy documents.
- **Integration with OpenAI and other APIs:** Enhance responses and automate workflows using state-of-the-art AI models.
- **Streamlit UI:** User-friendly web interface for interacting with your codex agent.

## Technologies Used

- Python 3
- Streamlit
- GEMINI API
- LangChain
- ChromaDB
- Various NLP and utility libraries (see `requirements.txt`)

## Getting Started

1. **Clone the repository:**
   ```
   git clone https://github.com/YangaRubushe/Personal_Codex_Agent.git
   cd personal-codex-agent
   ```

2. **Create and activate a virtual environment:**
   ```
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   - Create a `.env` file in the project root.
   - Add your API keys and configuration (see `.env.example` if available).

5. **Run the application:**
   ```
   streamlit run app.py
   ```

## Security

**Never commit your `.env` file or API keys to version control.**  
Always add `.env` to your `.gitignore`.

## License

This project is licensed under the MIT License.

---
