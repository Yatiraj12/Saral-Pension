from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict

from app.chains.qa_chain import run_qa_chain
from app.services.personalization import personalize_response


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "en"
    user_profile: Optional[Dict] = None


class ChatResponse(BaseModel):
    response: str


def is_greeting(text: str) -> bool:
    greetings = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    }
    return text.lower().strip() in greetings


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()

    if is_greeting(message):
        return ChatResponse(
            response="Hello, I’m Saral Pension Assistant. How can I assist you today?"
        )

    answer = run_qa_chain(
        question=message,
        language=request.language or "en"
    )

    answer = personalize_response(answer, request.user_profile)

    return ChatResponse(response=answer)
