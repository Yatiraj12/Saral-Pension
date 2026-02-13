from pathlib import Path
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from app.rag.retriever import retrieve_context
from app.services.language_service import translate_if_needed
from app.config import get_llm


PROMPT_PATH = Path("app/prompts/qa_prompt.txt")


def load_qa_prompt() -> PromptTemplate:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )


def run_qa_chain(
    question: str,
    language: str = "en"
) -> str:

    results: List[Tuple[Document, float]] = retrieve_context(
        query=question,
        sources=["qa", "schemes", "retirement"]
    )

    # =========================
    # 🔎 DEBUG SECTION (Added)
    # =========================
    print("\n===== RETRIEVAL DEBUG START =====")
    if not results:
        print("No documents retrieved.")
    else:
        for idx, (doc, score) in enumerate(results):
            print(f"\nResult {idx+1}")
            print("Score:", score)
            print("Content Preview:", doc.page_content[:300])
            print("-" * 60)
    print("===== RETRIEVAL DEBUG END =====\n")
    # =========================

    # Confidence thresholds (tuned for FAISS L2 distance)
    STRONG_THRESHOLD = 1.0
    MEDIUM_THRESHOLD = 1.6

    relevant_docs: List[Document] = []

    if results:
        best_score = results[0][1]
        print("Best Score:", best_score)  # 🔎 DEBUG

        if best_score < STRONG_THRESHOLD:
            # High confidence match
            relevant_docs = [
                doc for doc, score in results if score < STRONG_THRESHOLD
            ]

            mode_instruction = """
Use ONLY the official PFRDA context to answer.
Do not provide AI assumptions.
"""

        elif best_score < MEDIUM_THRESHOLD:
            # Medium confidence match
            relevant_docs = [
                doc for doc, score in results if score < MEDIUM_THRESHOLD
            ]

            mode_instruction = """
Use the official PFRDA context to answer.
If the answer is partially available, clarify based on context.
Avoid making unsupported assumptions.
"""

        else:
            # Very weak match
            relevant_docs = []

            mode_instruction = """
No clearly relevant official PFRDA data was found for this question.
Provide a professional AI-based retirement recommendation.
Clearly indicate that this is general guidance.
"""

    else:
        relevant_docs = []

        mode_instruction = """
No official PFRDA data was found for this question.
Provide a professional AI-based retirement recommendation.
Clearly indicate that this is general guidance.
"""

    if relevant_docs:
        context = "\n\n".join(doc.page_content for doc in relevant_docs)
    else:
        context = ""

    llm = get_llm()
    prompt_template = load_qa_prompt()

    prompt = prompt_template.format(
        context=context,
        question=question
    ) + mode_instruction

    response = llm.invoke(prompt)
    answer = response.content

    return translate_if_needed(answer, language)
