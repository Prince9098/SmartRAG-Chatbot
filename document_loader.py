from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader, CSVLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import TMP_DIR

def delete_temp_files():
    import glob, os
    files = glob.glob(TMP_DIR.as_posix() + "/*")
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting {f}: {e}")

def langchain_document_loader():
    documents = []
    txt_loader = DirectoryLoader(TMP_DIR.as_posix(), glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
    documents.extend(txt_loader.load())
    pdf_loader = DirectoryLoader(TMP_DIR.as_posix(), glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True)
    documents.extend(pdf_loader.load())
    csv_loader = DirectoryLoader(TMP_DIR.as_posix(), glob="**/*.csv", loader_cls=CSVLoader, show_progress=True, loader_kwargs={"encoding": "utf8"})
    documents.extend(csv_loader.load())
    doc_loader = DirectoryLoader(TMP_DIR.as_posix(), glob="**/*.docx", loader_cls=Docx2txtLoader, show_progress=True)
    documents.extend(doc_loader.load())
    return documents

def split_documents_to_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks
