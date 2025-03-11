from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database import get_db, User, UserSetting, SystemSetting
from src.api.schemas.users import UserSettingResponse, UserSettingUpdate
from src.api.schemas.settings import SystemSettingResponse, SystemSettingCreate, SystemSettingUpdate
from src.api.routes.auth import get_current_admin_user, get_current_active_user
from src.utils.encryption import encrypt_value, decrypt_value

# Router
router = APIRouter()


# User Settings Routes
@router.get("/user", response_model=UserSettingResponse)
async def get_user_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current user's settings."""
    settings = db.query(UserSetting).filter(UserSetting.user_id == current_user.id).first()
    
    # Create settings if they don't exist
    if not settings:
        settings = UserSetting(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings


@router.put("/user", response_model=UserSettingResponse)
async def update_user_settings(
    settings_update: UserSettingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update current user's settings."""
    settings = db.query(UserSetting).filter(UserSetting.user_id == current_user.id).first()
    
    # Create settings if they don't exist
    if not settings:
        settings = UserSetting(user_id=current_user.id)
        db.add(settings)
    
    # Update settings
    if settings_update.theme is not None:
        settings.theme = settings_update.theme
    
    if settings_update.default_llm_provider is not None:
        settings.default_llm_provider = settings_update.default_llm_provider
    
    if settings_update.default_ollama_model is not None:
        settings.default_ollama_model = settings_update.default_ollama_model
    
    db.commit()
    db.refresh(settings)
    return settings


# System Settings Routes (Admin only)
@router.get("/system", response_model=List[SystemSettingResponse])
async def get_system_settings(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Get all system settings (admin only)."""
    settings = db.query(SystemSetting).all()
    
    # Decrypt encrypted values
    for setting in settings:
        if setting.is_encrypted:
            setting.value = decrypt_value(setting.value)
    
    return settings


@router.get("/system/{key}", response_model=SystemSettingResponse)
async def get_system_setting(
    key: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Get a specific system setting (admin only)."""
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting with key '{key}' not found",
        )
    
    # Decrypt if encrypted
    if setting.is_encrypted:
        setting.value = decrypt_value(setting.value)
    
    return setting


@router.post("/system", response_model=SystemSettingResponse, status_code=status.HTTP_201_CREATED)
async def create_system_setting(
    setting: SystemSettingCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Create a new system setting (admin only)."""
    # Check if setting already exists
    existing_setting = db.query(SystemSetting).filter(SystemSetting.key == setting.key).first()
    if existing_setting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Setting with key '{setting.key}' already exists",
        )
    
    # Encrypt value if needed
    value = setting.value
    if setting.is_encrypted:
        value = encrypt_value(value)
    
    # Create new setting
    new_setting = SystemSetting(
        key=setting.key,
        value=value,
        is_encrypted=setting.is_encrypted,
    )
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    
    # Decrypt for response
    if new_setting.is_encrypted:
        new_setting.value = decrypt_value(new_setting.value)
    
    return new_setting


@router.put("/system/{key}", response_model=SystemSettingResponse)
async def update_system_setting(
    key: str,
    setting_update: SystemSettingUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update a system setting (admin only)."""
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting with key '{key}' not found",
        )
    
    # Update value
    if setting_update.value is not None:
        # Encrypt if needed
        value = setting_update.value
        if setting.is_encrypted:
            value = encrypt_value(value)
        setting.value = value
    
    # Update encryption status
    if setting_update.is_encrypted is not None and setting_update.is_encrypted != setting.is_encrypted:
        # If changing encryption status, we need to handle the value appropriately
        if setting_update.is_encrypted:
            # Encrypt the current value
            setting.value = encrypt_value(decrypt_value(setting.value) if setting.is_encrypted else setting.value)
        else:
            # Decrypt the current value
            setting.value = decrypt_value(setting.value) if setting.is_encrypted else setting.value
        
        setting.is_encrypted = setting_update.is_encrypted
    
    db.commit()
    db.refresh(setting)
    
    # Decrypt for response
    if setting.is_encrypted:
        setting.value = decrypt_value(setting.value)
    
    return setting


@router.delete("/system/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_setting(
    key: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a system setting (admin only)."""
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting with key '{key}' not found",
        )
    
    db.delete(setting)
    db.commit()
    return None