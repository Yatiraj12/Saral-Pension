import os
import numpy as np
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings

load_dotenv()

_embedding_model = None

class NormalizedHFEmbeddings(HuggingFaceEndpointEmbeddings):
    def embed_documents(self, texts):
        vectors = super().embed_documents(texts)
        return [self._normalize(v) for v in vectors]

    def embed_query(self, text):
        vector = super().embed_query(text)
        return self._normalize(vector)

    def _normalize(self, vector):
        arr = np.array(vector)
        norm = np.linalg.norm(arr)
        if norm == 0:
            return vector
        return (arr / norm).tolist()


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = NormalizedHFEmbeddings(
            model="sentence-transformers/paraphrase-MiniLM-L3-v2",
            huggingfacehub_api_token=os.getenv("HF_TOKEN"),
            task="feature-extraction"
        )

    return _embedding_model
