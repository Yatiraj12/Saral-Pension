import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.rag.embeddings import get_embedding_model


BASE_VECTORSTORE_DIR = "vectorstore"


def build_vectorstore(documents: list[Document], store_name: str) -> FAISS:
    embeddings = get_embedding_model()

    store_path = os.path.join(BASE_VECTORSTORE_DIR, store_name)
    os.makedirs(store_path, exist_ok=True)

    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(store_path)

    return vectorstore


def load_vectorstore(store_name: str) -> FAISS:
    embeddings = get_embedding_model()

    store_path = os.path.join(BASE_VECTORSTORE_DIR, store_name)

    if not os.path.exists(store_path):
        raise FileNotFoundError(f"Vectorstore '{store_name}' not found. Build it first.")

    return FAISS.load_local(
        store_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
