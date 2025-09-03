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
        else:
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
    return docs

def main():
    print("📥 Loading documents...")
    docs = load_documents()
    print(f"📄 Loaded {len(docs)} documents.")

    print("✂️ Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(docs)
    print(f"🔹 Created {len(chunks)} chunks.")

    print("🧠 Creating embeddings and vector DB...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)
    vectordb.persist()
    print(f"✅ Database created and saved in '{DB_DIR}'.")

if __name__ == "__main__":
    main()
