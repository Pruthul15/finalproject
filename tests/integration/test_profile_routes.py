"""Integration tests for profile routes."""
import pytest
from fastapi import status
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_get_profile_authenticated(client, auth_headers, db_session):
    """Test getting profile while authenticated"""
    response = client.get("/api/profile", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Verify profile has all required fields
    assert "username" in data
    assert "email" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "id" in data
    # Verify they're not empty
    assert data["username"]
    assert data["email"]


@pytest.mark.asyncio
async def test_get_profile_unauthenticated(client):
    """Test getting profile without authentication fails"""
    response = client.get("/api/profile")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_profile_success(client, auth_headers):
    """Test successfully updating profile"""
    update_data = {
        "username": "newusername",
        "email": "newemail@example.com",
        "first_name": "Jane",
        "last_name": "Smith"
    }
    response = client.put("/api/profile", json=update_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "newusername"
    assert data["email"] == "newemail@example.com"
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"


@pytest.mark.asyncio
async def test_update_profile_invalid_username(client, auth_headers):
    """Test updating profile with invalid username fails"""
    update_data = {
        "username": "ab",  # Too short
        "email": "newemail@example.com",
        "first_name": "Jane",
        "last_name": "Smith"
    }
    response = client.put("/api/profile", json=update_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_profile_invalid_email(client, auth_headers):
    """Test updating profile with invalid email fails"""
    update_data = {
        "username": "newusername",
        "email": "not-an-email",
        "first_name": "Jane",
        "last_name": "Smith"
    }
    response = client.put("/api/profile", json=update_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_profile_empty_name(client, auth_headers):
    """Test updating profile with empty name fails"""
    update_data = {
        "username": "newusername",
        "email": "newemail@example.com",
        "first_name": "",
        "last_name": "Smith"
    }
    response = client.put("/api/profile", json=update_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_change_password_success(client, auth_headers, test_user_data):
    """Test successfully changing password"""
    change_data = {
        "old_password": test_user_data["password"],
        "new_password": "NewPass@123",
        "confirm_password": "NewPass@123"
    }
    response = client.post("/api/change-password", json=change_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "Password changed successfully" in data["message"]


@pytest.mark.asyncio
async def test_change_password_wrong_old_password(client, auth_headers):
    """Test changing password with wrong old password fails"""
    change_data = {
        "old_password": "WrongPassword@123",
        "new_password": "NewPass@123",
        "confirm_password": "NewPass@123"
    }
    response = client.post("/api/change-password", json=change_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "Current password is incorrect" in data["detail"]


@pytest.mark.asyncio
async def test_change_password_passwords_dont_match(client, auth_headers, test_user_data):
    """Test changing password when passwords don't match fails"""
    change_data = {
        "old_password": test_user_data["password"],
        "new_password": "NewPass@123",
        "confirm_password": "DifferentPass@456"
    }
    response = client.post("/api/change-password", json=change_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_change_password_invalid_new_password(client, auth_headers, test_user_data):
    """Test changing password with invalid new password fails"""
    change_data = {
        "old_password": test_user_data["password"],
        "new_password": "short",
        "confirm_password": "short"
    }
    response = client.post("/api/change-password", json=change_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_change_password_unauthenticated(client):
    """Test changing password without authentication fails"""
    change_data = {
        "old_password": "OldPass@123",
        "new_password": "NewPass@123",
        "confirm_password": "NewPass@123"
    }
    response = client.post("/api/change-password", json=change_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_profile_unauthenticated(client):
    """Test updating profile without authentication fails"""
    update_data = {
        "username": "newusername",
        "email": "newemail@example.com",
        "first_name": "Jane",
        "last_name": "Smith"
    }
    response = client.put("/api/profile", json=update_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED