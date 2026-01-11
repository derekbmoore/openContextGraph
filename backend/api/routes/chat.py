"""Chat API routes"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str = ""
    agent: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # TODO: Integrate with agent system
    return ChatResponse(
        response=f"Echo: {request.message}",
        session_id=request.session_id or "new-session",
        agent=request.agent,
    )
