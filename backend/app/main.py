import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    description="A complete production-ready WhatsApp AI Business Agent API with RAG pipeline.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Set CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the dashboard domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include api router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "docs_url": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
