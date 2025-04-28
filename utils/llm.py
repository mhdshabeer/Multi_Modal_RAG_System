# utils/llm.py

from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config import LLM_MODEL

def initialize_llm():
    """Initializes the LLM."""
    return Ollama(model=LLM_MODEL)

def create_qa_chain(llm, retriever, prompt_template):
    """Creates a RetrievalQA chain."""
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )

def clean_llm_response(response):
    """Cleans the LLM response by removing unwanted tags."""
    import re
    return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()