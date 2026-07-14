from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict

class BusinessSettingsBase(BaseModel):
    business_name: str = "My AI Business"
    business_description: Optional[str] = None
    business_hours: Optional[Dict[str, str]] = Field(
        default={
            "monday": "09:00-18:00",
            "tuesday": "09:00-18:00",
            "wednesday": "09:00-18:00",
            "thursday": "09:00-18:00",
            "friday": "09:00-18:00",
            "saturday": "Closed",
            "sunday": "Closed"
        }
    )
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    address: Optional[str] = None
    greeting_message: str = "Hello! Welcome to our business. How can I help you today?"
    fallback_message: str = "I am sorry, but I do not have that information at the moment. Would you like me to connect you to a human representative?"

class PromptSettingsBase(BaseModel):
    system_prompt: str = "You are a professional AI assistant representing this business. Answer only using the business knowledge provided. Never hallucinate. Be polite. Keep responses concise. If the answer is unavailable in the retrieved context, respond with the fallback message."
    llm_temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(default=800, ge=1, le=4096)

class CombinedSettingsResponse(BaseModel):
    business: BusinessSettingsBase
    prompt: PromptSettingsBase
