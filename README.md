# Personal Codex Agent

## Overview

**Personal Codex Agent** is an AI-powered assistant that helps users interact with and manage their personal knowledge base. It leverages advanced language models, vector databases, and modern Python libraries to provide intelligent search, summarization, and automation for your documents and notes.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Show Your Thinking Artifacts](#show-your-thinking-artifacts)
  - [Prompt Histories](#prompt-histories)
  - [Agent Instructions](#agent-instructions)
  - [Sub-Agent Roles](#sub-agent-roles)
- [Technologies Used](#technologies-used)
- [Security](#security)
- [License](#license)

---

## Features

- **Natural Language Querying:** Ask questions in plain English and get relevant answers from your knowledge base.
- **Document Ingestion:** Easily add and organize documents, notes, and other resources.
- **Summarization:** Generate concise summaries of lengthy documents.
- **Multiple Response Modes:** Choose between interview, storytelling, fast facts, or humble brag styles.
- **Streamlit UI:** User-friendly web interface for interacting with your codex agent.
- **Secure API Key Handling:** Uses `.env` files for secrets, never committed to version control.

---

## Project Structure

```
personal-codex-agent/
│
├── app.py                # Main Streamlit application
├── ingest.py             # Document ingestion and vectorization script
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore file (should include .env)
├── README.md             # This documentation
├── data/                 # Folder for user documents (PDFs, txt, md, etc.)
├── db/                   # Vector database directory (auto-generated)
└── .env                  # Environment variables (not committed)
```

---

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/your-repo.git
cd personal-codex-agent
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Your `.env` File

Create a `.env` file in the project root with your API keys:

```
GEMINI_API_KEY=your-gemini-api-key
```

**Never commit your `.env` file!**

---

## Usage

### 1. Ingest Your Documents

Place your documents (PDF, txt, md) in the `data/` folder.

Run the ingestion script to process and vectorize your documents:

```sh
python ingest.py
```

### 2. Launch the Streamlit App

```sh
streamlit run app.py
```

Open the provided local URL in your browser to interact with your Personal Codex Agent.

---

## Configuration

- **data/**: Place all documents you want to query here.
- **db/**: Vector database is stored here (auto-generated).
- **.env**: Store your API keys and secrets here.
- **requirements.txt**: All dependencies are listed here.

---

## Show Your Thinking Artifacts

### Prompt Histories

- **User Prompt Example:**  
  “What are your strongest technical skills?”  
  “Tell me about your most impressive project in a storytelling style.”

- **System Prompt Example:**  
  “You are a helpful AI assistant. Respond in a professional interview style unless otherwise specified.”

### Agent Instructions

- **Main Agent:**  
  - Retrieve relevant document chunks using semantic search.
  - Use conversation memory to maintain context.
  - Format responses according to user-selected style (interview, storytelling, fast facts, humble brag).
  - Always cite the source document if possible.

### Sub-Agent Roles

- **Document Ingestion Sub-Agent:**  
  - Loads and preprocesses documents from the `data/` folder.
  - Splits documents into context-aware chunks.
  - Embeds chunks using HuggingFace models.
  - Stores embeddings in ChromaDB.

- **Chat Interface Sub-Agent:**  
  - Handles user input and session state.
  - Retrieves relevant chunks from the vector database.
  - Constructs prompts for the Gemini API.
  - Displays responses in the Streamlit UI.

---

## Technologies Used

- **Python 3**
- **Streamlit** (UI)
- **LangChain** (retrieval, memory, prompt management)
- **ChromaDB** (vector database)
- **HuggingFace Embeddings** (semantic search)
- **Google Gemini API** (language model)
- **dotenv** (environment variable management)

---

## Security

- **API keys and secrets** are stored in `.env` and never committed to version control.
- `.env` is included in `.gitignore` by default.

---

## License

This project is licensed under the MIT License.

---

## Example Files

### app.py

```python
from dotenv import load_dotenv
import os
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from google import genai

# --- Load Gemini API Key ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- Vector DB Setup ---
DB_DIR = "db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# --- Memory ---
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory()

# --- Streamlit UI ---
st.title("Personal Codex Agent")
query = st.text_input("Ask a question about your knowledge base:")
if st.button("Ask"):
    # Retrieve relevant docs and generate response (pseudo-code)
    results = vectordb.similarity_search(query)
    context = "\n".join([doc.page_content for doc in results])
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    response = client.generate(prompt)
    st.write(response)
```

### ingest.py

```python
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = "data"
DB_DIR = "db"

def load_documents():
    docs = []
    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif file.endswith(".txt") or file.endswith(".md"):
            loader = TextLoader(path)
            docs.extend(loader.load())
    return docs

def preprocess_documents(docs):
    # Example: remove empty docs
    return [doc for doc in docs if doc.page_content.strip()]

def create_smart_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_documents([doc]))
    return chunks

def main():
    print("🚀 Starting enhanced document ingestion...")
    docs = load_documents()
    if not docs:
        print("No documents found in data/.")
        return
    processed_docs = preprocess_documents(docs)
    chunks = create_smart_chunks(processed_docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedding_function=embeddings, persist_directory=DB_DIR)
    vectordb.persist()
    print(f"✅ Ingested {len(chunks)} chunks into the vector database.")

if __name__ == "__main__":
    main()
```

---

## .gitignore

```
.env
db/
__pycache__/
*.pyc
```

---

## requirements.txt

See the provided `requirements.txt` file for all dependencies.

---
