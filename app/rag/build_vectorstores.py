import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from app.rag.embeddings import get_embedding_model


BASE_DATA_PATH = Path("data/nps_docs/processed")
VECTORSTORE_PATH = Path("vectorstore")


def load_json_documents(json_path: Path) -> List[Document]:
    if not json_path.exists():
        raise FileNotFoundError(f"Missing file: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ FIX: handle {"chunks": [...]} format
    if isinstance(data, dict) and "chunks" in data:
        chunks = data["chunks"]
    else:
        chunks = data

    documents = []

    for chunk in chunks:
        if not isinstance(chunk, dict):
            continue

        text = chunk.get("text") or chunk.get("content")
        if not text:
            continue

        metadata = {
            "source": chunk.get("source", json_path.stem),
            "category": chunk.get("category"),
            "language": chunk.get("language", "en"),
            "chunk_id": chunk.get("chunk_id") or chunk.get("id")
        }

        documents.append(
            Document(
                page_content=text,
                metadata=metadata
            )
        )

    return documents


def build_vectorstore(name: str, json_file: str):
    print(f"\nBuilding vectorstore: {name}")

    json_path = BASE_DATA_PATH / json_file
    output_path = VECTORSTORE_PATH / name

    documents = load_json_documents(json_path)
    print(f"Loaded {len(documents)} documents")

    embeddings = get_embedding_model()

    vectorstore = FAISS.from_documents(documents, embeddings)

    output_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(output_path))

    print(f"Saved vectorstore to: {output_path}")


def main():
    build_vectorstore("qa", "qa_chunks.json")
    build_vectorstore("schemes", "schemes_chunks.json")
    build_vectorstore("retirement", "retirement_chunks.json")


if __name__ == "__main__":
    main()
