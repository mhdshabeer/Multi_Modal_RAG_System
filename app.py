# app.py

import streamlit as st
from utils.file_processing import process_files
from utils.embeddings import initialize_embeddings, create_vector_db, save_vector_db, load_vector_db
from utils.llm import initialize_llm, create_qa_chain, clean_llm_response
from utils.chat import initialize_chat_history, display_chat_history, add_message_to_history
from langchain.prompts import PromptTemplate
from config import SEARCH_K

# --- MUST BE FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="DocuMind",
    page_icon="\U0001F50D",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Purple-Black UI ---
def inject_custom_css():
    st.markdown(
        """
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            
            /* Main background and text */
            .stApp {
                background-color: #0a0a0f !important;
                color: #e0e0e0 !important;
                font-family: 'Poppins', sans-serif;
            }

            /* Container structure */
            .main .block-container {
                padding-top: 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }

            /* App header section */
            .app-header {
                background: linear-gradient(90deg, #13131f, #1e1e2f);
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 4px 20px rgba(123, 97, 255, 0.15);
                border: 1px solid #3a2f6b;
            }

            /* Sidebar */
            .stSidebar {
                background-color: #13131f !important;
                border-right: 1px solid #3a2f6b;
            }
            
            .stSidebar [data-testid="stSidebarNav"] {
                background-color: #13131f !important;
            }

            /* Chat messages */
            [data-testid="stChatMessage"] {
                margin-bottom: 15px;
            }
            
            [data-testid="stChatMessage"] > div:first-child {
                background-color: #1e1e2f !important;
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                border-left: 3px solid #6940ff;
            }
            
            [data-testid="stChatMessage"] > div:last-child {
                background: linear-gradient(135deg, #6940ff 0%, #8e61ff 100%) !important;
                color: white !important;
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 0 4px 12px rgba(123, 97, 255, 0.3);
            }

            /* Input box */
            .stTextInput input {
                background-color: #1e1e2f !important;
                color: white !important;
                border: 1px solid #3a2f6b !important;
                border-radius: 12px;
                padding: 14px 18px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            
            .stTextInput input:focus {
                border-color: #8e61ff !important;
                box-shadow: 0 0 0 2px rgba(142, 97, 255, 0.25) !important;
            }

            section[data-testid="stChatInput"] {
                background: linear-gradient(180deg, rgba(10, 10, 15, 0), #0a0a0f);
                padding: 20px 0;
                position: sticky;
                bottom: 0;
            }

            /* Buttons */
            .stButton button {
                background: linear-gradient(135deg, #6940ff 0%, #8e61ff 100%) !important;
                color: white !important;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: 600;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(123, 97, 255, 0.3);
                width: 100%;
            }
            
            .stButton button:hover {
                background: linear-gradient(135deg, #5e39e0 0%, #7d56e5 100%) !important;
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(123, 97, 255, 0.4);
            }

            /* File uploader */
            .stFileUploader {
                background-color: #1e1e2f !important;
                border: 2px dashed #3a2f6b !important;
                border-radius: 12px;
                padding: 20px;
                transition: all 0.3s ease;
            }
            
            .stFileUploader:hover {
                border-color: #8e61ff !important;
            }

            /* Headers */
            h1 {
                color: #ffffff !important;
                font-weight: 700;
                font-size: 36px;
                background: linear-gradient(to right, #6940ff, #a37eff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 8px;
            }
            
            h2 {
                color: #a37eff !important;
                font-weight: 600;
                font-size: 24px;
                margin-top: 5px;
            }
            
            h3 {
                color: #8e61ff !important;
                font-weight: 500;
            }

            /* Caption */
            .stCaption {
                color: #a0a0b8 !important;
                font-size: 16px;
                letter-spacing: 0.5px;
                margin-bottom: 25px;
            }

            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #1e1e2f !important;
                border-radius: 12px;
                padding: 5px;
            }
            
            .stTabs [data-baseweb="tab"] {
                border-radius: 8px;
                padding: 8px 16px;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #6940ff !important;
                color: white !important;
            }

            /* Spinner */
            .stSpinner > div {
                border-color: #8e61ff transparent transparent !important;
            }

            /* Success/Error messages */
            .stSuccess {
                background-color: rgba(123, 97, 255, 0.1) !important;
                color: #a37eff !important;
                border: 1px solid #6940ff;
                border-radius: 10px;
                padding: 10px 15px !important;
            }
            
            .stError {
                background-color: rgba(255, 82, 82, 0.1) !important;
                color: #ff5252 !important;
                border: 1px solid #ff5252;
                border-radius: 10px;
                padding: 10px 15px !important;
            }

            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 6px;
                background-color: #13131f;
            }
            
            ::-webkit-scrollbar-thumb {
                background-color: #3a2f6b;
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background-color: #6940ff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- App Header with Logo and Title ---
def render_header():
    header_html = """
    <div class="app-header">
        <h1>DocuMind AI</h1>
        <p class="stCaption">Your intelligent document assistant powered by AI</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# --- Initialize QA Chain ---
def initialize_qa_chain():
    if "vector_db" not in st.session_state or st.session_state.vector_db is None:
        return None
    
    retriever = st.session_state.vector_db.as_retriever(search_kwargs={"k": SEARCH_K})
    prompt_template = PromptTemplate.from_template(
        "Context: {context}\nQuestion: {question}\nAnswer:"
    )
    return create_qa_chain(
        llm=initialize_llm(),
        retriever=retriever,
        prompt_template=prompt_template
    )

# --- Process Uploaded Files ---
def process_uploaded_files(pdfs, images, audios):
    with st.spinner("Processing documents..."):
        all_texts = []
        if pdfs:
            all_texts.extend(process_files(pdfs, "pdf"))
        if images:
            all_texts.extend(process_files(images, "image"))
        if audios:
            all_texts.extend(process_files(audios, "audio"))

        if all_texts:
            st.session_state.vector_db = create_vector_db(all_texts, initialize_embeddings())
            save_vector_db(st.session_state.vector_db)
            st.sidebar.success("Documents processed successfully!")
        else:
            st.sidebar.error("No text could be extracted from files.")

# --- Handle User Query ---
def handle_query(query):
    qa_chain = initialize_qa_chain()
    if not qa_chain:
        return "Please upload and process documents first."
    
    try:
        result = qa_chain.invoke({"query": query})
        return clean_llm_response(result["result"])
    except Exception as e:
        return f"Error generating response: {str(e)}"

# --- Main App Components ---
def render_sidebar():
    with st.sidebar:
        st.header("Document Manager")
        
        st.subheader("Upload Files")
        tab1, tab2, tab3 = st.tabs(["PDF", "Images", "Audio"])
        
        with tab1:
            pdfs = st.file_uploader("PDFs", type="pdf", accept_multiple_files=True)
        with tab2:
            images = st.file_uploader("Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        with tab3:
            audios = st.file_uploader("Audio", type=["mp3", "wav"], accept_multiple_files=True)
        
        if st.button("Process Files", use_container_width=True):
            process_uploaded_files(pdfs, images, audios)

def render_chat():
    # Create a container for the chat window
    chat_container = st.container()
    
    with chat_container:
        # Display all existing messages (including the latest ones)
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.write(message["content"])
    
    # Handle new user input
    if prompt := st.chat_input("Ask about your documents..."):
        # Add user message to history and display immediately
        add_message_to_history("user", prompt, "👤")
        
        # Display assistant response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = handle_query(prompt)
                st.write(response)
        
        # Add assistant response to history
        add_message_to_history("assistant", response, "🤖")
        
        # Force immediate rerun to show all messages
        st.rerun()

# --- Main App Flow ---
def main():
    inject_custom_css()
    initialize_chat_history()
    
    if "vector_db" not in st.session_state:
        st.session_state.vector_db = None
    
    render_header()
    
    render_sidebar()
    render_chat()

if __name__ == "__main__":
    main()