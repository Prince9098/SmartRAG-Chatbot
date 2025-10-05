from langchain_community.vectorstores import Chroma
from embeddings import select_embeddings_model
from document_loader import langchain_document_loader, split_documents_to_chunks, delete_temp_files
from config import LOCAL_VECTOR_STORE_DIR, TMP_DIR
import streamlit as st
import os, logging

def create_vectorstore_retriever(vector_store, search_type="similarity", k=10):
    search_kwargs = {"k": k}
    retriever = vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
    return retriever

def create_new_vectorstore():
    with st.spinner("Creating vectorstore..."):
        error_messages = []
        if not st.session_state.get('openai_api_key') and not st.session_state.get('google_api_key') and not st.session_state.get('hf_api_key'):
            error_messages.append(f"insert your {st.session_state.LLM_provider} API key")
        if not st.session_state.get('uploaded_file_list'):
            error_messages.append("select documents to upload")
        if st.session_state.get('vector_store_name', '') == "":
            error_messages.append("provide a Vectorstore name")
        if error_messages:
            if len(error_messages) == 1:
                st.error(f"Please {error_messages[0]}.")
            else:
                st.error(f"Please {', '.join(error_messages[:-1])}, and {error_messages[-1]}.")
            return
        try:
            delete_temp_files()
            for uploaded_file in st.session_state.uploaded_file_list:
                temp_file_path = os.path.join(TMP_DIR.as_posix(), uploaded_file.name)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())
            documents = langchain_document_loader()
            if not documents:
                st.error("No documents were loaded. Please check your files.")
                return
            chunks = split_documents_to_chunks(documents)
            embeddings = select_embeddings_model()
            persist_directory = os.path.join(LOCAL_VECTOR_STORE_DIR.as_posix(), st.session_state.vector_store_name)
            st.session_state.vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
            st.success(f"✅ Vectorstore **{st.session_state.vector_store_name}** created successfully!")
            st.session_state.retriever = create_vectorstore_retriever(vector_store=st.session_state.vector_store, search_type="similarity", k=10)
            # Create conversational chain and memory
            from llm import create_conversational_chain
            st.session_state.chain, st.session_state.memory = create_conversational_chain(
                retriever=st.session_state.retriever,
                language=st.session_state.assistant_language,
            )
        except Exception as e:
            logging.error(f"Error creating vectorstore: {e}")
            error_str = str(e)
            if (
                "429" in error_str or
                "quota" in error_str.lower() or
                "rate limit" in error_str.lower() or
                "exceeded" in error_str.lower()
            ):
                st.error("API quota exceeded or too many requests. Please check your API key, plan, and billing details.")
            elif "Expecting value: line 1 column 1 (char 0)" in error_str:
                logging.error("Likely cause: Empty or invalid response from API. Check your API key, rate limits, or service availability.")
                st.error("API Error: Received empty or invalid response. Please check your API key, rate limits, or if the service is down.")
            elif any(x in error_str.lower() for x in ["api key", "unauthorized", "invalid api", "missing api", "usage"]):
                st.error(f"API Error: {error_str}")
            else:
                st.error(f"An error occurred: {error_str}")

def load_existing_vectorstore():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    selected_path = filedialog.askdirectory(master=root)
    if not selected_path:
        st.info("Please select a valid path.")
        return
    with st.spinner("Loading vectorstore..."):
        try:
            st.session_state.selected_vectorstore_name = selected_path.split("/")[-1]
            embeddings = select_embeddings_model()
            st.session_state.vector_store = Chroma(embedding_function=embeddings, persist_directory=selected_path)
            st.session_state.retriever = create_vectorstore_retriever(vector_store=st.session_state.vector_store, search_type="similarity", k=10)
            # Create conversational chain and memory
            from llm import create_conversational_chain
            st.session_state.chain, st.session_state.memory = create_conversational_chain(
                retriever=st.session_state.retriever,
                language=st.session_state.assistant_language,
            )
            st.success(f"✅ **{st.session_state.selected_vectorstore_name}** loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading vectorstore: {e}")
            error_str = str(e)
            if (
                "429" in error_str or
                "quota" in error_str.lower() or
                "rate limit" in error_str.lower() or
                "exceeded" in error_str.lower()
            ):
                st.error("API quota exceeded or too many requests. Please check your API key, plan, and billing details.")
            elif "Expecting value: line 1 column 1 (char 0)" in error_str:
                logging.error("Likely cause: Empty or invalid response from API. Check your API key, rate limits, or service availability.")
                st.error("API Error: Received empty or invalid response. Please check your API key, rate limits, or if the service is down.")
            elif any(x in error_str.lower() for x in ["api key", "unauthorized", "invalid api", "missing api", "usage"]):
                st.error(f"API Error: {error_str}")
            else:
                st.error(f"Error loading vectorstore: {error_str}")
