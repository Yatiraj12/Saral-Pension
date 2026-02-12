import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document


JSON_FOLDER = Path("data/nps_docs/processed")


def load_documents() -> List[Document]:
    if not JSON_FOLDER.exists():
        raise FileNotFoundError(f"JSON folder not found at {JSON_FOLDER}")

    documents: List[Document] = []

    for file_path in JSON_FOLDER.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle both formats:
        # 1. List of chunks
        # 2. {"chunks": [...]}
        chunks = data.get("chunks") if isinstance(data, dict) else data

        for chunk in chunks:
            text = chunk.get("text") or chunk.get("content")
            if not text:
                continue

            metadata = {
                "source": chunk.get("source", file_path.stem),
                "chunk_id": chunk.get("chunk_id") or chunk.get("id"),
                "language": chunk.get("language", "en"),
                "category": chunk.get("category")
            }

            documents.append(
                Document(
                    page_content=text,
                    metadata=metadata
                )
            )

    return documents
