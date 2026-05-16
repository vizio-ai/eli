from fastapi import APIRouter
from pydantic import BaseModel
from integrations.slack import send_message, get_users

router = APIRouter()

class SlackMessage(BaseModel):
    channel: str
    text: str

@router.post("/send")
def send(msg: SlackMessage):
    return send_message(msg.channel, msg.text)

@router.get("/users")
def users():
    return get_users()
