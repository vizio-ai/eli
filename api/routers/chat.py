from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.eli import chat

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    stream: bool = False

@router.post("/")
def chat_endpoint(req: ChatRequest):
    messages = [m.model_dump() for m in req.messages]
    if req.stream:
        return StreamingResponse(chat(messages, stream=True), media_type="text/plain")
    return {"reply": chat(messages)}
