# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime # Import the datetime library

# This is for creating a user (data we receive)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# --- NEW ---
# This is for sending user data back (data we send)
# It should never include the password.
class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime