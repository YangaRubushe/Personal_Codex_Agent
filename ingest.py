import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

DATA_DIR = "data"
DB_DIR = "db"

def load_documents():
    """Load all documents with enhanced metadata"""
    docs = []
    
    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)
        
        try:
            if file.endswith(".pdf"):
                print(f"📄 Loading PDF: {file}")
                loader = PyPDFLoader(path)
                pdf_docs = loader.load()
                
                # Add metadata to PDF documents
                for i, doc in enumerate(pdf_docs):
                    doc.metadata.update({
                        "source_file": file,
                        "file_type": "pdf",
                        "document_type": "cv" if "cv" in file.lower() else "document",
                        "page_number": i + 1
                    })
                
                docs.extend(pdf_docs)
                print(f"   ✅ Loaded {len(pdf_docs)} pages from {file}")
                
            elif file.endswith((".txt", ".md")):
                print(f"📝 Loading text file: {file}")
                loader = TextLoader(path, encoding="utf-8")
                text_docs = loader.load()
                
                # Add metadata to text documents
                for doc in text_docs:
                    # Determine document type based on filename
                    if "project" in file.lower():
                        doc_type = "project"
                    elif "values" in file.lower():
                        doc_type = "values"
                    elif "cv" in file.lower():
                        doc_type = "cv"
                    else:
                        doc_type = "general"
                    
                    doc.metadata.update({
                        "source_file": file,
                        "file_type": file.split('.')[-1],
                        "document_type": doc_type
                    })
                
                docs.extend(text_docs)
                print(f"   ✅ Loaded {file}")
                
        except Exception as e:
            print(f"   ❌ Error loading {file}: {str(e)}")
            continue
    
    return docs

def preprocess_documents(docs):
    """Clean and preprocess documents"""
    processed_docs = []
    
    for doc in docs:
        # Clean text content
        content = doc.page_content.strip()
        
        # Skip empty documents
        if not content or len(content) < 50:
            continue
            
        # Remove excessive whitespace
        content = ' '.join(content.split())
        
        # Create new document with cleaned content
        processed_doc = Document(
            page_content=content,
            metadata=doc.metadata
        )
        
        processed_docs.append(processed_doc)
    
    return processed_docs

def create_smart_chunks(docs):
    """Create contextually aware chunks"""
    all_chunks = []
    
    for doc in docs:
        doc_type = doc.metadata.get("document_type", "general")
        
        # Different chunking strategies based on document type
        if doc_type == "cv":
            # Smaller chunks for CV to preserve specific skills/experiences
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", ";", ",", " "]
            )
        elif doc_type == "project":
            # Medium chunks for projects to keep related info together
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=300,
                separators=["\n\n", "\n", ".", " "]
            )
        elif doc_type == "values":
            # Larger chunks for values to maintain context
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=600,
                chunk_overlap=150,
                separators=["\n\n", "\n", ".", " "]
            )
        else:
            # Default chunking
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=250
            )
        
        # Split the document
        doc_chunks = splitter.split_documents([doc])
        
        # Add chunk metadata
        for i, chunk in enumerate(doc_chunks):
            chunk.metadata.update({
                "chunk_id": i,
                "total_chunks": len(doc_chunks),
                "chunk_type": f"{doc_type}_chunk"
            })
        
        all_chunks.extend(doc_chunks)
        print(f"   📝 Created {len(doc_chunks)} chunks from {doc.metadata['source_file']} ({doc_type})")
    
    return all_chunks

def enhance_chunks_with_context(chunks):
    """Add contextual information to chunks"""
    enhanced_chunks = []
    
    for chunk in chunks:
        doc_type = chunk.metadata.get("document_type", "general")
        source_file = chunk.metadata.get("source_file", "unknown")
        
        # Add context prefix based on document type
        context_prefix = ""
        if doc_type == "cv":
            context_prefix = "[CV/RESUME CONTENT] "
        elif doc_type == "project":
            context_prefix = f"[PROJECT DETAILS from {source_file}] "
        elif doc_type == "values":
            context_prefix = "[PERSONAL VALUES & PRINCIPLES] "
        
        # Enhanced content with context
        enhanced_content = context_prefix + chunk.page_content
        
        # Create enhanced chunk
        enhanced_chunk = Document(
            page_content=enhanced_content,
            metadata=chunk.metadata
        )
        
        enhanced_chunks.append(enhanced_chunk)
    
    return enhanced_chunks

def main():
    print("🚀 Starting enhanced document ingestion...")
    print("=" * 50)
    
    # Step 1: Load documents
    print("\n📥 Step 1: Loading documents...")
    docs = load_documents()
    
    if not docs:
        print("❌ No documents found! Make sure files are in the 'data' directory.")
        return
    
    print(f"📄 Successfully loaded {len(docs)} document sections.")
    
    # Step 2: Preprocess documents
    print("\n🧹 Step 2: Preprocessing documents...")
    processed_docs = preprocess_documents(docs)
    print(f"✨ Cleaned and processed {len(processed_docs)} documents.")
    
    # Step 3: Create smart chunks
    print("\n✂️ Step 3: Creating contextually aware chunks...")
    chunks = create_smart_chunks(processed_docs)
    print(f"🔹 Created {len(chunks)} total chunks.")
    
    # Step 4: Enhance with context
    print("\n🎯 Step 4: Enhancing chunks with context...")
    enhanced_chunks = enhance_chunks_with_context(chunks)
    print(f"⚡ Enhanced {len(enhanced_chunks)} chunks with contextual information.")
    
    # Step 5: Create vector database
    print("\n🧠 Step 5: Creating embeddings and vector database...")
    
    # Remove existing database
    if os.path.exists(DB_DIR):
        import shutil
        shutil.rmtree(DB_DIR)
        print("🗑️ Removed existing database.")
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Create vector database
    vectordb = Chroma.from_documents(
        documents=enhanced_chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )
    
    # Persist the database
    vectordb.persist()
    
    print(f"✅ Vector database created successfully!")
    print(f"   📁 Location: {DB_DIR}")
    print(f"   📊 Total chunks: {len(enhanced_chunks)}")
    print(f"   🎯 Ready for intelligent retrieval!")
    
    # Print summary by document type
    print("\n📋 INGESTION SUMMARY:")
    print("-" * 30)
    doc_types = {}
    for chunk in enhanced_chunks:
        doc_type = chunk.metadata.get("document_type", "general")
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
    
    for doc_type, count in doc_types.items():
        print(f"   {doc_type.upper()}: {count} chunks")
    
    print("\n🎉 Ingestion completed successfully!")
    print("   Your personal Codex is ready to answer questions!")

if __name__ == "__main__":
    main()