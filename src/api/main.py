from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from src.database import init_db
from src.api.routes import auth, users, chats, documents, settings, rag

# Initialize FastAPI app
app = FastAPI(
    title="Doogie RAG Chatbot API",
    description="API for Doogie, a hybrid RAG chatbot system",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chats"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])

# Mount static files for frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend/dist")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

# Root endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": app.version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)