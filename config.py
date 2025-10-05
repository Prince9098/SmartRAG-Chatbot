import logging
from pathlib import Path

list_LLM_providers = [
    ":rainbow[**OpenAI**]",
    "**Google Generative AI**",
    ":hugging_face: **HuggingFace**",
]

dict_welcome_message = {
    "english": "How can I assist you today?"
}

TMP_DIR = Path(__file__).resolve().parent.joinpath("data", "tmp")
LOCAL_VECTOR_STORE_DIR = Path(__file__).resolve().parent.joinpath("data", "vector_stores")

# Logging setup
logging.basicConfig(
    filename="rag_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
