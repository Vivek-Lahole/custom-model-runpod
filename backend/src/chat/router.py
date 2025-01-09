from src.chat.models import ChatResponse, ChatRequest
from fastapi import APIRouter
from src.chat.services import get_chat_response

chat_router = APIRouter()


@chat_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    resp = get_chat_response(request.message, request.custom_dataset)
    return ChatResponse(message=resp)
