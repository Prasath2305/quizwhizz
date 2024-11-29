from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def get_vectorstore(text_chunks):
    """Convert text chunks into embeddings and store them in a FAISS vector store."""
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore
