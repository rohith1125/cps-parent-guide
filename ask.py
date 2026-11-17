from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document
from llama_index.core import VectorStoreIndex
from pinecone import Pinecone
from pinecone import ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
import openai
from llama_index.llms.openai import OpenAI
import torch
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core import PromptTemplate
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import json
import os
from llama_index.core.query_engine import RetrieverQueryEngine

# Initialize Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
if not pinecone_api_key:
    st.error("PINECONE_API_KEY environment variable not set!")
    st.stop()

pc_index = "askneu"  # Changed to askneu index
pc = Pinecone(api_key=pinecone_api_key)
pinecone_index = pc.Index(pc_index)

# Initialize embeddings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="Snowflake/snowflake-arctic-embed-m-v1.5", trust_remote_code=True
)

# Streamlit UI configuration
st.set_page_config(page_title="CPS Parent Guide", layout="wide")

# Sidebar for API key and chat management
with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("Enter OpenAI API Key:", type="password")
    
    st.markdown("---")
    st.header("Chat Management")
    
    # Initialize session state for chat management
    if "chats" not in st.session_state:
        st.session_state.chats = {}
    
    if "current_chat_id" not in st.session_state:
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat_id = chat_id
        st.session_state.chats[chat_id] = {
            "id": chat_id,
            "title": "Chat 1",
            "history": []
        }
    
    # New Chat button
    if st.button("+ New Chat"):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat_id = chat_id
        st.session_state.chats[chat_id] = {
            "id": chat_id,
            "title": f"Chat {len(st.session_state.chats)+1}",
            "history": []
        }
    
    # Display existing chats
    st.subheader("Previous Chats")
    for chat_id in list(st.session_state.chats.keys()):
        if st.button(
            f"📝 {st.session_state.chats[chat_id]['title']}",
            key=f"chat_{chat_id}",
            use_container_width=True
        ):
            st.session_state.current_chat_id = chat_id

# Main chat interface
st.title("🏫 CPS Parent Guide: Your Education Assistant")
st.markdown("### Get answers about Chicago Public Schools - enrollment, programs, policies, and more!")

# Quick help section
with st.expander("💡 What can I ask about?"):
    st.markdown("""
    **Common topics you can ask about:**
    - 📚 **Enrollment & Registration**: How to enroll your child, required documents, deadlines
    - 🏫 **School Information**: Find schools, programs, ratings, and contact info
    - 📋 **Academic Programs**: IB, STEM, arts, special education, gifted programs
    - 🚌 **Transportation**: Bus routes, eligibility, safety information
    - 🍽️ **Nutrition**: Free/reduced lunch, meal programs, dietary accommodations
    - 🏥 **Health Services**: Immunizations, health screenings, medical forms
    - 📅 **Calendar & Events**: School year calendar, holidays, parent meetings
    - 💰 **Financial Aid**: Scholarships, fee waivers, payment plans
    - 🎯 **Testing & Assessment**: Standardized tests, report cards, progress tracking
    - 🔧 **Parent Resources**: How to get involved, volunteer opportunities, parent councils
    """)

# Initialize current chat
current_chat = st.session_state.chats[st.session_state.current_chat_id]

# Display chat history
for message in current_chat["history"]:
    role = "Human" if isinstance(message, HumanMessage) else "AI"
    with st.chat_message(role):
        st.markdown(message.content)

# Chat input
user_query = st.chat_input("Ask about CPS schools, enrollment, programs, or any education topic...")

if user_query:
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar!")
        st.stop()
    
    # Set OpenAI API key
    openai.api_key = openai_api_key
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        api_key=openai_api_key,
        request_timeout=360.0,
        temperature=0.3,
        num_beams=3
    )
    
    # Add user message to chat history
    current_chat["history"].append(HumanMessage(user_query))
    
    # Display user message
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    # Initialize query engine components
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store, 
        embed_model=Settings.embed_model
    )
    
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
        embed_model=Settings.embed_model
    )
    
    qa_prompt = PromptTemplate(
        "You are a helpful assistant for Chicago Public Schools (CPS) parent queries. "
        "You provide accurate, up-to-date information about CPS schools, enrollment, programs, policies, and resources for parents.\n\n"
        "Context:\n{context_str}\n\n"
        "Question: {query_str}\n\n"
        "Answer: Provide a comprehensive, parent-friendly response. Include specific details about CPS policies, "
        "practical steps parents can take, and relevant contact information when available. "
        "If the information isn't in the context, mention that parents should contact their school directly or visit cps.edu for the most current information."
    )
    
    response_synthesizer = get_response_synthesizer(
        response_mode="compact",
        llm=Settings.llm,
        text_qa_template=qa_prompt
    )
    
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
    
    # Generate response
    with st.spinner("Searching CPS information..."):
        try:
            response = query_engine.query(user_query)
            ai_response = str(response)
        except Exception as e:
            ai_response = f"I'm having trouble accessing the CPS information right now. Please try again or contact your school directly. Error: {str(e)}"
    
    # Add and display AI response
    current_chat["history"].append(AIMessage(ai_response))
    with st.chat_message("AI"):
        st.markdown(ai_response)

# Footer with additional resources
st.markdown("---")
st.markdown("""
**📞 Need more help?**
- **CPS Main Office**: (773) 553-1000
- **CPS Website**: [cps.edu](https://cps.edu)
- **Parent Portal**: [parent.cps.edu](https://parent.cps.edu)
- **Emergency Hotline**: (773) 535-4400

**💡 Pro Tip**: For the most current and specific information about your child's school, always contact the school directly or check the official CPS website.
""")
