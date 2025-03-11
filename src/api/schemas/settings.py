from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class SystemSettingBase(BaseModel):
    """Base system setting schema."""
    key: str
    value: str
    is_encrypted: bool = False


class SystemSettingCreate(SystemSettingBase):
    """Schema for system setting creation."""
    pass


class SystemSettingUpdate(BaseModel):
    """Schema for system setting update."""
    value: Optional[str] = None
    is_encrypted: Optional[bool] = None


class SystemSettingResponse(SystemSettingBase):
    """Schema for system setting response."""
    id: str

    class Config:
        from_attributes = True


class SystemPromptBase(BaseModel):
    """Base system prompt schema."""
    name: str
    content: str
    description: Optional[str] = None
    is_default: bool = False


class SystemPromptCreate(SystemPromptBase):
    """Schema for system prompt creation."""
    pass


class SystemPromptUpdate(BaseModel):
    """Schema for system prompt update."""
    name: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None


class SystemPromptResponse(SystemPromptBase):
    """Schema for system prompt response."""
    id: str

    class Config:
        from_attributes = True