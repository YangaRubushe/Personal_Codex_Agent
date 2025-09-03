import os
from dotenv import load_dotenv
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from google import genai
import time



# --- Load Gemini API Key ---
load_dotenv()  # load variables from .env

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("❌ Please set your GEMINI_API_KEY environment variable.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- Vector DB Setup ---
DB_DIR = "db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# --- Memory ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="question")

# --- Prompt Template ---
SYSTEM_PROMPT = """
I am Yanga Rubushe, a BSc Graduate in Computer Science and Statistics and currently an Honours student at UWC, 
as well as an ALX Software Engineering graduate specialising in backend development.

I always respond fluently, confidently, and in first person. 
When I talk about my work, I highlight my projects such as NexGen Learn AI-powered learning platform and CineNex a netflix clone , 
my technical skills (Java, Python, R, SAS, Machine Learning, AI, Typescript, Node.js, SQL, NoSQL, Git, Docker, RESTful APIs, Github, Agile methodologies), 
and my values (resilience, curiosity, and continuous learning). 

I speak like a professional but approachable Honours Computer Science student, 
keeping my answers clear, natural, and authentic to my journey. 

Question: {question}
"""


prompt = PromptTemplate(input_variables=["question"], template=SYSTEM_PROMPT)

# --- Gemini Query Function ---
def ask_gemini(question: str) -> str:
    resp = client.models.generate_content(
        model="gemini-2.5-flash",  # can switch to "gemini-2.5-pro" for deeper reasoning
        contents=question
    )
    return resp.text

# --- Streamlit UI ---
st.set_page_config(page_title="Yanga Codex Agent", page_icon="🤖")
st.title("🤖 Personal Codex Agent - Gemini Edition")
st.write("Ask me anything about my skills, projects, and journey!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Typing effect
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

    # Add context from DB
    retriever = vectordb.as_retriever()
    context_docs = retriever.get_relevant_documents(query)
    context_text = "\n".join([doc.page_content for doc in context_docs[:3]])

    # Format with system prompt
    formatted_query = prompt.format(question=f"{query}\n\nContext:\n{context_text}")

    # Get Gemini response
    answer = ask_gemini(formatted_query)

    # Stream the answer
    stream_answer(answer)

    # Save to history
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": answer})
