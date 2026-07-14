from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MessageText(BaseModel):
    body: str

class MessageMedia(BaseModel):
    id: str
    mime_type: str
    sha256: Optional[str] = None
    filename: Optional[str] = None
    caption: Optional[str] = None

class MessageContactProfile(BaseModel):
    name: str

class MessageContact(BaseModel):
    profile: MessageContactProfile
    wa_id: str

class MessageStatus(BaseModel):
    id: str
    status: str # 'sent', 'delivered', 'read', 'failed'
    recipient_id: str
    timestamp: str
    conversation: Optional[Dict[str, Any]] = None
    pricing: Optional[Dict[str, Any]] = None

class WebhookMessage(BaseModel):
    from_phone: str = Field(alias="from")
    id: str
    timestamp: str
    type: str # 'text', 'image', 'video', 'audio', 'document', 'voice', 'location', 'contacts'
    text: Optional[MessageText] = None
    image: Optional[MessageMedia] = None
    audio: Optional[MessageMedia] = None
    voice: Optional[MessageMedia] = None
    video: Optional[MessageMedia] = None
    document: Optional[MessageMedia] = None
    contacts: Optional[List[Dict[str, Any]]] = None
    location: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True

class WebhookMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class WebhookValue(BaseModel):
    messaging_product: str
    metadata: WebhookMetadata
    contacts: Optional[List[MessageContact]] = None
    messages: Optional[List[WebhookMessage]] = None
    statuses: Optional[List[MessageStatus]] = None

class WebhookChange(BaseModel):
    value: WebhookValue
    field: str

class WebhookEntry(BaseModel):
    id: str
    changes: List[WebhookChange]

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[WebhookEntry]
