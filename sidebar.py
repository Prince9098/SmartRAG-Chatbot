import streamlit as st
from config import list_LLM_providers, dict_welcome_message

def create_sidebar():
    with st.sidebar:
        st.caption("🚀 A RAG chatbot powered by 🔗 Langchain with Vectorstore Retriever Only")
        st.write("")
        llm_chooser = st.radio(
            "Select LLM Provider",
            list_LLM_providers,
            captions=[
                "[OpenAI pricing page](https://openai.com/pricing)",
                "Rate limit: 60 requests per minute.",
                "**Free access.**",
            ],
        )
        st.divider()
        if llm_chooser == list_LLM_providers[0]:
            st.session_state.LLM_provider = "OpenAI"
            st.session_state.openai_api_key = st.text_input(
                "OpenAI API Key - [Get an API key](https://platform.openai.com/account/api-keys)",
                type="password",
                placeholder="sk-...",
            )
            models = ["gpt-3.5-turbo", "gpt-4-turbo-preview", "gpt-3.5-turbo-0125"]
        elif llm_chooser == list_LLM_providers[1]:
            st.session_state.LLM_provider = "Google"
            st.session_state.google_api_key = st.text_input(
                "Google API Key - [Get an API key](https://makersuite.google.com/app/apikey)",
                type="password",
                placeholder="AIza...",
            )
            models = ["gemini-pro"]
        else:
            st.session_state.LLM_provider = "HuggingFace"
            st.session_state.hf_api_key = st.text_input(
                "HuggingFace API key - [Get an API key](https://huggingface.co/settings/tokens)",
                type="password",
                placeholder="hf_...",
            )
            models = ["mistralai/Mistral-7B-Instruct-v0.2"]
        with st.expander("**Models and Parameters**"):
            st.session_state.selected_model = st.selectbox("Choose model", models)
            st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
            st.session_state.top_p = st.slider("Top P", 0.0, 1.0, 0.95, 0.05)
        st.divider()
        st.session_state.assistant_language = st.selectbox(
            "Assistant Language", 
            list(dict_welcome_message.keys())
        )
        st.divider()
        st.info("ℹ️ This app uses **Vectorstore Retriever ONLY** for document retrieval.")
