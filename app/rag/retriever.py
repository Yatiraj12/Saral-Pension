from pathlib import Path
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.rag.embeddings import get_embedding_model


# ✅ Absolute base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
VECTORSTORE_BASE = BASE_DIR / "vectorstore"


def load_vectorstore(source: str) -> FAISS:
    path = VECTORSTORE_BASE / source

    print("Loading vectorstore from:", path.resolve())  # 🔎 DEBUG

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
    k: int = 4,
    score_threshold: float = 1.3
) -> List[Tuple[Document, float]]:

    all_docs: List[Tuple[Document, float]] = []

    for source in sources:
        vectorstore = load_vectorstore(source)

        results = vectorstore.similarity_search_with_score(query, k=k)

        print(f"Raw results from {source}:", len(results))  # 🔎 DEBUG

        for doc, score in results:
            print("Score:", score)  # 🔎 DEBUG

            if score < score_threshold:
                all_docs.append((doc, score))

    all_docs.sort(key=lambda x: x[1])

    return all_docs
