# utils/embeddings.py

import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDINGS_MODEL

def initialize_embeddings():
    """Initializes the embeddings model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)

def create_vector_db(texts, embeddings):
    """Creates a FAISS vector database from text chunks."""
    return FAISS.from_texts(texts, embeddings)

def save_vector_db(vector_db, cache_dir="cache"):
    """Saves the FAISS index and metadata to disk."""
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    vector_db.save_local(cache_dir)

def load_vector_db(embeddings, cache_dir="cache"):
    """Loads the FAISS index and metadata from disk."""
    if os.path.exists(cache_dir):
        return FAISS.load_local(cache_dir, embeddings)
    return None