from langchain_core.prompts import PromptTemplate
from app.config import get_llm



TRANSLATION_PROMPT = PromptTemplate(
    input_variables=["text", "language"],
    template="""
Translate the following text into the target language.

Rules:
- Do not change numbers, tax section names, or pension terminology.
- Preserve meaning exactly.

Target Language:
{language}

Text:
{text}

Translated Text:
"""
)


def translate_if_needed(text: str, language: str) -> str:
    if not language or language.lower() == "en":
        return text

    llm = get_llm()
    prompt = TRANSLATION_PROMPT.format(text=text, language=language)
    response = llm.invoke(prompt)


    return response.content.strip()
