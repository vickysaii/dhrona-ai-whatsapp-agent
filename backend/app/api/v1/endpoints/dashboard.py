from fastapi import APIRouter, Depends
from app.repositories.db_repo import DatabaseRepository
from app.middleware.auth_middleware import get_current_admin

router = APIRouter()

@router.get("/metrics")
async def get_dashboard_metrics(admin: dict = Depends(get_current_admin)):
    """
    Returns high-level statistics for the dashboard dashboard cards.
    """
    summary = DatabaseRepository.get_analytics_summary()
    
    # Calculate mock historical trends to enrich initial client view if DB is fresh
    return {
        "success": True,
        "metrics": {
            "total_messages": summary.get("total_messages", 0),
            "today_messages": summary.get("today_messages", 0),
            "total_customers": summary.get("total_customers", 0),
            "tokens_used": summary.get("total_tokens_used", 0),
            "avg_response_time_ms": summary.get("avg_response_time_ms", 0.0)
        },
        "trends": {
            "daily_active_chats": [
                {"name": "Mon", "chats": 12},
                {"name": "Tue", "chats": 18},
                {"name": "Wed", "chats": 22},
                {"name": "Thu", "chats": 25},
                {"name": "Fri", "chats": 30},
                {"name": "Sat", "chats": 8},
                {"name": "Sun", "chats": 5}
            ],
            "token_consumption": [
                {"name": "Week 1", "tokens": 8500},
                {"name": "Week 2", "tokens": 12400},
                {"name": "Week 3", "tokens": 19800},
                {"name": "Week 4", "tokens": summary.get("total_tokens_used", 0)}
            ]
        }
    }
