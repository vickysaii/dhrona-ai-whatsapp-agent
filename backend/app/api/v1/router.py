from fastapi import APIRouter
from app.api.v1.endpoints import (
    webhook,
    auth,
    settings,
    upload,
    conversations,
    dashboard,
    chat
)

api_router = APIRouter()

# Include endpoint sub-routers
api_router.include_router(webhook.router, tags=["Webhook"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(upload.router, prefix="/kb", tags=["Knowledge Base"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# NEW
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])