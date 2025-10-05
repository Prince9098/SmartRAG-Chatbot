import streamlit as st
from config import dict_welcome_message

def clear_chat_history():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": dict_welcome_message[st.session_state.assistant_language],
        }
    ]
    if 'memory' in st.session_state:
        try:
            st.session_state.memory.clear()
        except:
            pass

def get_response(prompt):
    try:
        import re, logging
        response = st.session_state.chain.invoke({"question": prompt})
        source_docs = response.get("source_documents", [])
        def is_relevant(doc, question):
            question_words = set(re.findall(r"\w+", question.lower()))
            doc_words = set(re.findall(r"\w+", doc.page_content.lower()))
            stopwords = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "of", "and", "or", "to", "for", "with", "by", "as", "from", "that", "this", "it", "be", "can", "will", "has", "have", "had", "but", "not", "do", "does", "did", "if", "so", "such"}
            question_words = {w for w in question_words if w not in stopwords and len(w) > 2}
            doc_words = {w for w in doc_words if w not in stopwords and len(w) > 2}
            overlap = question_words & doc_words
            return len(overlap) >= 2
        relevant_docs = [doc for doc in source_docs if doc.page_content.strip()]
        if not source_docs:
            answer = "Sorry, I can't answer that because it is not related to the provided documents. Please ask something relevant to the attached documents."
        else:
            answer = response["answer"]
            if st.session_state.LLM_provider == "HuggingFace":
                if "\nAnswer: " in answer:
                    answer = answer[answer.find("\nAnswer: ") + len("\nAnswer: ") :]
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            st.markdown(answer)
            if relevant_docs:
                with st.expander("**Source documents**"):
                    documents_content = ""
                    for i, document in enumerate(relevant_docs):
                        page = f" (Page: {document.metadata.get('page', 'N/A')})"
                        source = document.metadata.get('source', 'Unknown')
                        documents_content += f"**Source {i+1}: {source}{page}**\n\n"
                        documents_content += document.page_content + "\n\n---\n\n"
                    st.markdown(documents_content)
    except Exception as e:
        import logging
        logging.error(f"Error getting response: {e}")
        error_str = str(e)
        if (
            "429" in error_str or
            "quota" in error_str.lower() or
            "rate limit" in error_str.lower() or
            "exceeded" in error_str.lower()
        ):
            st.error("API quota exceeded or too many requests. Please check your API key, plan, and billing details.")
            st.info("Tip: Check your API key, plan, and billing status if you see quota or rate limit errors.")
        elif "Expecting value: line 1 column 1 (char 0)" in error_str:
            logging.error("Likely cause: Empty or invalid response from API. Check your API key, rate limits, or service availability.")
            st.error("API Error: Received empty or invalid response. Please check your API key, rate limits, or if the service is down.")
        elif any(x in error_str.lower() for x in ["api key", "unauthorized", "invalid api", "missing api", "usage"]):
            st.error(f"API Error: {error_str}")
        else:
            st.error(f"Error getting response: {error_str}")
