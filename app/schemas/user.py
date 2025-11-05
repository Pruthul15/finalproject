"""
User-related Pydantic schemas for validation and serialization.
"""
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    first_name: str
    last_name: str

    @field_validator('username')
    @classmethod
    def username_valid(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, _, -')
        return v

    @field_validator('password')
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('Password must contain special character (!@#$%^&*)')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def name_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v.strip()

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "SecurePass@123",
            "confirm_password": "SecurePass@123",
            "first_name": "John",
            "last_name": "Doe"
        }
    })


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johndoe",
            "password": "SecurePass@123"
        }
    })


class UserResponse(BaseModel):
    """Schema for user response."""
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile (not password)."""
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, _, -')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def name_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v.strip()

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johnupdated",
            "email": "john.updated@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
    })


class PasswordChange(BaseModel):
    """Schema for changing password."""
    old_password: str
    new_password: str
    confirm_password: str

    @field_validator('old_password')
    @classmethod
    def old_password_required(cls, v):
        if not v:
            raise ValueError('Current password is required')
        return v

    @field_validator('new_password')
    @classmethod
    def new_password_valid(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('Password must contain special character (!@#$%^&*)')
        return v

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "old_password": "OldPass@123",
            "new_password": "NewPass@456",
            "confirm_password": "NewPass@456"
        }
    })


class UserProfileResponse(BaseModel):
    """Schema for user profile response."""
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)