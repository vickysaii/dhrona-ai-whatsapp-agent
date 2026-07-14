from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.business_agent import BusinessAgent

router = APIRouter()


class ChatRequest(BaseModel):
    phone: str
    message: str
    name: str | None = None


@router.post("/")
async def chat(payload: ChatRequest):
    """
    Test endpoint for the AI Agent.
    Later the WhatsApp webhook will call the same BusinessAgent.
    """

    response = BusinessAgent.process_message(
        customer_phone=payload.phone,
        customer_message=payload.message,
        customer_name=payload.name,
    )

    return response