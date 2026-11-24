from fastapi import APIRouter
#from backend.app.models.user_model import User
from fastapi import Depends
from backend.app.utils.auth import get_current_user

from backend.app.models.user_model import User, LoginRequest
from backend.app.database.mongodb import db
from backend.app.utils.hashing import hash_password
from backend.app.utils.hashing import verify_password
from backend.app.utils.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/register")
def register_user(user: User):

    users_collection = db["users"]

    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        return {"message": "Email already registered"}

    # Save user
    user_data = user.model_dump()
    user_data["password"] = hash_password(user.password)
    users_collection.insert_one(user_data)

    return {"message": "User Registered Successfully"}

@router.post("/login")
def login(user: LoginRequest):
    users_collection = db["users"]

    existing_user = users_collection.find_one({"email": user.email})

    if not existing_user:
        return {"message": "User not found"}

    if not verify_password(user.password, existing_user["password"]):
        return {"message": "Invalid password"}

    token = create_access_token({
        "email": existing_user["email"],
        "role": existing_user["role"]
    })

    return {
        "message": "Login Successful",
        "access_token": token,
        "role": existing_user["role"]
    }

@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "message": "Welcome!",
        "user": current_user
    }