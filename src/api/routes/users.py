from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db, User, UserStatus, UserRole, UserSetting
from src.api.schemas.users import UserResponse, UserUpdate, UserApproval
from src.api.routes.auth import get_current_admin_user, get_current_active_user

# Router
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Get all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/pending", response_model=List[UserResponse])
async def get_pending_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Get all pending users (admin only)."""
    users = db.query(User).filter(User.status == UserStatus.PENDING).all()
    return users


@router.put("/approve/{user_id}", response_model=UserResponse)
async def approve_user(
    user_id: str,
    approval: UserApproval,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Approve or reject a pending user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.status != UserStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not pending approval",
        )
    
    # Update user status based on approval
    if approval.approved:
        user.status = UserStatus.ACTIVE
    else:
        user.status = UserStatus.INACTIVE
    
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Update a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update user fields
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    
    if user_update.role is not None:
        user.role = UserRole(user_update.role)
    
    if user_update.status is not None:
        user.status = UserStatus(user_update.status)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )
    
    db.delete(user)
    db.commit()
    return None


@router.put("/me/update", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update current user's information."""
    # Only allow updating full_name for regular users
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    db.commit()
    db.refresh(current_user)
    return current_user