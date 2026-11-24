from pydantic import BaseModel, EmailStr
from typing import Literal
class User(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal["candidate", "recruiter"]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str