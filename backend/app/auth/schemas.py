from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_id: Optional[str] = None
    department: Optional[str] = None
    job_title: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class UserResponse(BaseModel):
    id: str
    email: str
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    company_id: Optional[str]
    department: Optional[str]
    job_title: Optional[str]
    role: str
    status: str
    email_verified: bool
    mfa_enabled: bool
    subscription_tier: str
    created_at: datetime
    class Config:
        from_attributes = True

class PasswordReset(BaseModel):
    email: EmailStr

class MFAVerify(BaseModel):
    code: str

class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None
