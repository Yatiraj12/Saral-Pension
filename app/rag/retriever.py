from pathlib import Path
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.rag.embeddings import get_embedding_model


VECTORSTORE_BASE = Path("vectorstore")


def load_vectorstore(source: str) -> FAISS:
    path = VECTORSTORE_BASE / source
    if not path.exists():
        raise FileNotFoundError(f"Vectorstore not found for source: {source}")

    embeddings = get_embedding_model()
    return FAISS.load_local(
        str(path),
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_context(
    query: str,
    sources: List[str],
    k: int = 4
) -> List[Tuple[Document, float]]:

    all_docs: List[Tuple[Document, float]] = []

    for source in sources:
        vectorstore = load_vectorstore(source)

        results = vectorstore.similarity_search_with_score(query, k=k)

        for doc, score in results:
            all_docs.append((doc, score))

    return all_docs
