import streamlit as st
from sidebar import create_sidebar
from vectorstore import create_new_vectorstore, load_existing_vectorstore
from utils import clear_chat_history, get_response
from config import dict_welcome_message

def main():
    create_sidebar()
    tab1, tab2 = st.tabs(["📤 Create New Vectorstore", "📂 Load Existing Vectorstore"])
    with tab1:
        st.subheader("Upload Documents and Create Vectorstore")
        st.session_state.uploaded_file_list = st.file_uploader(
            "**Select documents**",
            accept_multiple_files=True,
            type=["pdf", "txt", "docx", "csv"],
        )
        st.session_state.vector_store_name = st.text_input(
            "**Vectorstore Name**",
            placeholder="my_vectorstore",
        )
        if st.button("🚀 Create Vectorstore", type="primary"):
            create_new_vectorstore()
    with tab2:
        st.subheader("Load Existing Vectorstore")
        st.write("Click the button below to select a vectorstore directory:")
        if st.button("📁 Select Vectorstore Directory", type="primary"):
            if not st.session_state.get('openai_api_key') and not st.session_state.get('google_api_key') and not st.session_state.get('hf_api_key'):
                st.error(f"Please insert your {st.session_state.LLM_provider} API key first.")
            else:
                load_existing_vectorstore()
    st.divider()
    col1, col2 = st.columns([7, 3])
    with col1:
        st.subheader("💬 Chat with Your Data")
    with col2:
        st.button("🗑️ Clear Chat History", on_click=clear_chat_history)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "How can I assist you today?",
            }
        ]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input("Ask a question about your documents..."):
        if not st.session_state.get('openai_api_key') and not st.session_state.get('google_api_key') and not st.session_state.get('hf_api_key'):
            st.info(f"Please insert your {st.session_state.LLM_provider} API key to continue.")
            st.stop()
        if 'chain' not in st.session_state:
            st.warning("⚠️ Please create or load a vectorstore first!")
            st.stop()
        with st.spinner("Thinking..."):
            get_response(prompt)
