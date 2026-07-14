from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.settings import CombinedSettingsResponse, BusinessSettingsBase, PromptSettingsBase
from app.repositories.db_repo import DatabaseRepository
from app.middleware.auth_middleware import get_current_admin
from typing import List, Dict, Any

router = APIRouter()

@router.get("", response_model=CombinedSettingsResponse)
async def get_settings(admin: dict = Depends(get_current_admin)):
    """
    Fetches the combined business configurations and prompt guidelines.
    """
    business = DatabaseRepository.get_business_settings()
    prompt = DatabaseRepository.get_prompt_settings()
    return {
        "business": business,
        "prompt": prompt
    }

@router.put("/business", response_model=BusinessSettingsBase)
async def update_business_settings(payload: BusinessSettingsBase, admin: dict = Depends(get_current_admin)):
    """
    Updates general business information and greeting messages.
    """
    settings_dict = payload.model_dump()
    settings_dict["id"] = "default"
    updated = DatabaseRepository.update_business_settings(settings_dict)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update business settings"
        )
    return updated

@router.put("/prompt", response_model=PromptSettingsBase)
async def update_prompt_settings(payload: PromptSettingsBase, admin: dict = Depends(get_current_admin)):
    """
    Updates the system instructions, temperature and limits of the AI Agent.
    """
    settings_dict = payload.model_dump()
    settings_dict["id"] = "default"
    updated = DatabaseRepository.update_prompt_settings(settings_dict)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update prompt settings"
        )
    return updated

# FAQ MANAGEMENT
@router.get("/faqs")
async def get_faqs(admin: dict = Depends(get_current_admin)):
    """
    Retrieves the custom manual Q&A list.
    """
    return DatabaseRepository.get_faqs()

@router.post("/faqs")
async def create_faq(question: str, answer: str, admin: dict = Depends(get_current_admin)):
    """
    Creates a direct Q&A record in database.
    """
    faq = DatabaseRepository.create_faq(question, answer)
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create FAQ"
        )
    return faq

@router.delete("/faqs/{faq_id}")
async def delete_faq(faq_id: str, admin: dict = Depends(get_current_admin)):
    """
    Removes a direct Q&A record from the database.
    """
    success = DatabaseRepository.delete_faq(faq_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete FAQ"
        )
    return {"success": True}
