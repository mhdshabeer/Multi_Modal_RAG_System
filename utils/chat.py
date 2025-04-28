# utils/chat.py

import streamlit as st

def initialize_chat_history():
    """Initializes the chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

def display_chat_history():
    """Displays the chat history."""
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

def add_message_to_history(role, content, avatar):
    """Adds a message to the chat history."""
    st.session_state["messages"].append({"role": role, "content": content, "avatar": avatar})