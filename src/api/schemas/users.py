from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    role: str
    status: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for user update."""
    full_name: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


class UserApproval(BaseModel):
    """Schema for user approval."""
    approved: bool = True
    

class UserSettingBase(BaseModel):
    """Base user setting schema."""
    theme: Optional[str] = "dark"
    default_llm_provider: Optional[str] = None
    default_ollama_model: Optional[str] = None


class UserSettingResponse(UserSettingBase):
    """Schema for user setting response."""
    id: str
    user_id: str

    class Config:
        from_attributes = True


class UserSettingUpdate(UserSettingBase):
    """Schema for user setting update."""
    pass