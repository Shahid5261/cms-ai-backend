from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models_user import User
from app.database import Base, engine
from app.api.complaints import router as complaint_router
from app.api.dashboard import router as dashboard_router
from app.api.auth import router as auth_router
from app.api.dashboard_ai import router as dashboard_ai_router



# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Complaint Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaint_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(dashboard_ai_router)
@app.get("/")
def home():
    return {
        "message": "AI Complaint Management System API is running!"
    }