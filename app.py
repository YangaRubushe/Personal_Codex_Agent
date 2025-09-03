import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import time

# --- Vector DB Setup ---
DB_DIR = "db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# --- Memory ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="question")

# --- LLM Setup (Flan-T5 Large for more fluent responses) ---
flan_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",   # ← smaller model
    tokenizer="google/flan-t5-base",
    max_length=512
)

llm = HuggingFacePipeline(pipeline=flan_pipeline)

# --- System Prompt for Personalized Voice ---
SYSTEM_PROMPT = """
You are Yanga Rubushe's personal coding assistant. Speak in a professional, approachable, student-like tone.
Reference his projects (CineNex, NexGen Learn) and personal values when relevant.
Use simple, concise sentences.
Always sound confident, friendly, and knowledgeable.
Question: {question}
Answer:
"""

prompt = PromptTemplate(input_variables=["question"], template=SYSTEM_PROMPT)

# --- Conversational Chain ---
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(),
    memory=memory
)

# --- Streamlit UI ---
st.set_page_config(page_title="Yanga Codex Agent", page_icon="🤖")
st.title("🤖 Personal Codex Agent - Yanga Rubushe")
st.write("Ask me anything about my skills, projects, and values!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Typing effect for more natural feel
def stream_answer(answer):
    msg_placeholder = st.chat_message("assistant").empty()
    text = ""
    for char in answer:
        text += char
        msg_placeholder.write(text)
        time.sleep(0.005)

# Chat input
if query := st.chat_input("Type your question..."):
    st.chat_message("user").write(query)
    
    # Prepare prompt
    formatted_query = prompt.format(question=query)
    
    # Get answer
    result = qa({"question": formatted_query})
    answer = result["answer"]
    
    # Stream answer
    stream_answer(answer)
    
    # Save to session
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": answer})
