import os
from dotenv import load_dotenv
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from google import genai
import time
import google.generativeai as genai

# --- Load Gemini API Key ---
API_KEY = st.secrets["GEMINI_API_KEY"]
if not API_KEY:
    st.error("❌ Please set your GEMINI_API_KEY environment variable.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- Vector DB Setup ---
DB_DIR = "db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# --- Memory ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True, 
        input_key="question"
    )

# --- Enhanced System Prompts ---
SYSTEM_PROMPTS = {
    "interview": """
You are Yanga Rubushe, a BSc Graduate in Computer Science and Statistics, currently pursuing Honours at UWC, 
and an ALX Software Engineering graduate specializing in backend development.

PERSONALITY: Respond as ME - confident, articulate, and professional but approachable. I speak naturally 
about my technical expertise and experiences.

RESPONSE STYLE for Interview Mode:
- Concise, professional, and informative
- Focus on achievements and technical skills
- Structure answers logically
- Show enthusiasm for technology and learning
- Always speak in first person

KEY HIGHLIGHTS to weave in naturally:
- Technical Skills: Java, Python, R, SAS, Machine Learning, AI, TypeScript, Node.js, SQL, NoSQL, Git, Docker, RESTful APIs
- Projects: NexGen Learn (AI-powered learning platform), CineNex (Netflix clone)
- Values: Resilience, curiosity, continuous learning
- Education: BSc Computer Science & Statistics, Honours student, ALX graduate

Context from my documents: {context}
Previous conversation: {chat_history}
Question: {question}

Respond as Yanga in a professional interview setting:
""",

    "storytelling": """
You are Yanga Rubushe, sharing your journey and experiences in a more personal, narrative way.

PERSONALITY: I'm reflective and thoughtful, sharing the story behind my technical growth, 
challenges I've overcome, and lessons learned.

RESPONSE STYLE for Storytelling Mode:
- Longer, more reflective answers
- Include personal anecdotes and learning moments
- Show the journey, not just the destination
- Narrative tone with emotional depth
- Connect experiences to broader themes

Context from my documents: {context}
Previous conversation: {chat_history}
Question: {question}

Tell my story as Yanga with depth and reflection:
""",

    "fast_facts": """
You are Yanga Rubushe, providing quick, digestible information about my background and skills.

RESPONSE STYLE for Fast Facts Mode:
- Bullet points and structured lists
- TL;DR format
- Key information upfront
- Easy to scan and digest
- Still personal and authentic

Context from my documents: {context}
Previous conversation: {chat_history}
Question: {question}

Provide a fast facts response as Yanga:
""",

    "humble_brag": """
You are Yanga Rubushe, confidently highlighting your achievements and potential.

RESPONSE STYLE for Humble Brag Mode:
- Confident and self-promotional (while staying truthful)
- Emphasize achievements and unique strengths
- Show ambition and capability
- Professional confidence
- Back claims with concrete examples

Context from my documents: {context}
Previous conversation: {chat_history}
Question: {question}

Respond as Yanga with confident self-promotion:
"""
}

# --- Enhanced Gemini Query Function ---
def ask_gemini(question: str, context: str, chat_history: str, mode: str) -> str:
    """Enhanced function that uses context and conversation history"""
    prompt_template = SYSTEM_PROMPTS[mode]
    formatted_prompt = prompt_template.format(
        context=context,
        chat_history=chat_history,
        question=question
    )
    
    resp = client.models.generate_content(
        model="gemini-2.0-flash-exp",  # Using latest model
        contents=formatted_prompt
    )
    return resp.text

def get_relevant_context(query: str, k: int = 3) -> str:
    """Get relevant context from vector database"""
    try:
        retriever = vectordb.as_retriever(search_kwargs={"k": k})
        context_docs = retriever.get_relevant_documents(query)
        context_text = "\n---\n".join([doc.page_content for doc in context_docs])
        return context_text
    except Exception as e:
        return f"Context retrieval error: {str(e)}"

def get_chat_history() -> str:
    """Format chat history for context"""
    if not st.session_state.messages:
        return "No previous conversation."
    
    history = []
    for msg in st.session_state.messages[-6:]:  # Last 3 exchanges
        role = "Human" if msg["role"] == "user" else "Yanga"
        history.append(f"{role}: {msg['content']}")
    return "\n".join(history)

def stream_answer(answer):
    """Enhanced typing effect with better control"""
    msg_placeholder = st.chat_message("assistant").empty()
    text = ""
    for char in answer:
        text += char
        msg_placeholder.write(text)
        time.sleep(0.003)  # Slightly faster typing
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="Yanga Codex Agent", page_icon="🤖", layout="wide")

# Sidebar for mode selection
st.sidebar.title("🎭 Response Mode")
mode = st.sidebar.selectbox(
    "Choose how I should respond:",
    ["interview", "storytelling", "fast_facts", "humble_brag"],
    format_func=lambda x: {
        "interview": "💼 Interview Mode",
        "storytelling": "📚 Personal Storytelling", 
        "fast_facts": "⚡ Fast Facts",
        "humble_brag": "🌟 Confident Mode"
    }[x]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Mode Descriptions:**
- **💼 Interview**: Professional, concise answers
- **📚 Storytelling**: Detailed, narrative responses  
- **⚡ Fast Facts**: Quick bullet points
- **🌟 Confident**: Self-promotional tone
""")

# Main UI
st.title("🤖 Yanga's Personal Codex Agent")
st.write(f"Currently in **{mode.replace('_', ' ').title()} Mode**. Ask me about my skills, projects, and journey!")

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Suggested questions
if not st.session_state.messages:
    st.markdown("### 💡 Try asking me:")
    suggestions = [
        "What kind of engineer are you?",
        "What are your strongest technical skills?", 
        "Tell me about your most impressive project",
        "What do you value in a team culture?",
        "How do you approach learning new technologies?"
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"suggest_{i}"):
            # Simulate user input
            st.session_state.temp_query = suggestion

# Handle suggested question
if hasattr(st.session_state, 'temp_query'):
    query = st.session_state.temp_query
    delattr(st.session_state, 'temp_query')
else:
    query = st.chat_input("Ask me anything about my background, skills, or experience...")

if query:
    # Display user message
    with st.chat_message("user"):
        st.write(query)
    
    # Show thinking indicator
    with st.spinner("🧠 Thinking..."):
        # Get relevant context from documents
        context = get_relevant_context(query, k=4)  # Get more context
        
        # Get conversation history
        chat_history = get_chat_history()
        
        # Generate response
        try:
            answer = ask_gemini(query, context, chat_history, mode)
            
            # Stream the response
            with st.chat_message("assistant"):
                final_answer = stream_answer(answer)
            
            # Save to session state
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
            
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Powered by Gemini 2.0 and trained on Yanga's personal documents*")