from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import streamlit as st

def select_embeddings_model():
    if st.session_state.LLM_provider == "OpenAI":
        embeddings = OpenAIEmbeddings(api_key=st.session_state.openai_api_key)
    elif st.session_state.LLM_provider == "Google":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=st.session_state.google_api_key)
    elif st.session_state.LLM_provider == "HuggingFace":
        embeddings = HuggingFaceInferenceAPIEmbeddings(api_key=st.session_state.hf_api_key, model_name="thenlper/gte-large")
    return embeddings
