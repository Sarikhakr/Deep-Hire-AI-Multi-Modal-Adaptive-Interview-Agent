from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Welcome to DeepHire AI 🚀",
        "status": "Backend Running Successfully"
    }