from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.home import router as home_router
from backend.app.database.mongodb import db
from backend.app.routes.auth import router as auth_router
from backend.app.routes.resume import router as resume_router
from backend.app.routes import interview


app = FastAPI(
    title="DeepHire AI API",
    description="Backend API for DeepHire AI",
    version="1.0.0"
)


# CORS - Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(home_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(interview.router)