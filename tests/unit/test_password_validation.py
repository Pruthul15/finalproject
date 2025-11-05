"""Unit tests for password validation schemas."""
import pytest
from pydantic import ValidationError
from app.schemas.user import PasswordChange, UserProfileUpdate


class TestPasswordChangeValidation:
    """Test PasswordChange schema validation."""

    def test_password_change_valid(self):
        """Test valid password change passes validation"""
        valid_pwd = PasswordChange(
            old_password="OldPass@123",
            new_password="NewPass@456",
            confirm_password="NewPass@456"
        )
        assert valid_pwd.new_password == "NewPass@456"
        assert valid_pwd.old_password == "OldPass@123"

    def test_password_too_short(self):
        """Test password too short fails"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="OldPass@123",
                new_password="Pass@1",
                confirm_password="Pass@1"
            )
        assert "at least 8 characters" in str(exc_info.value)

    def test_password_no_uppercase(self):
        """Test password without uppercase fails"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="OldPass@123",
                new_password="newpass@456",
                confirm_password="newpass@456"
            )
        assert "uppercase" in str(exc_info.value)

    def test_password_no_lowercase(self):
        """Test password without lowercase fails"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="OldPass@123",
                new_password="NEWPASS@456",
                confirm_password="NEWPASS@456"
            )
        assert "lowercase" in str(exc_info.value)

    def test_password_no_digit(self):
        """Test password without digit fails"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="OldPass@123",
                new_password="NewPass@NoDigit",
                confirm_password="NewPass@NoDigit"
            )
        assert "digit" in str(exc_info.value)

    def test_password_no_special_char(self):
        """Test password without special char fails"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="OldPass@123",
                new_password="NewPass456",
                confirm_password="NewPass456"
            )
        assert "special character" in str(exc_info.value)

    def test_passwords_dont_match(self):
        """Test passwords that don't match fail"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="OldPass@123",
                new_password="NewPass@456",
                confirm_password="Different@456"
            )
        assert "do not match" in str(exc_info.value)

    def test_old_password_required(self):
        """Test old password is required"""
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(
                old_password="",
                new_password="NewPass@456",
                confirm_password="NewPass@456"
            )
        assert "required" in str(exc_info.value)


class TestUserProfileUpdateValidation:
    """Test UserProfileUpdate schema validation."""

    def test_profile_update_valid(self):
        """Test valid profile update passes validation"""
        update = UserProfileUpdate(
            username="newuser",
            email="new@example.com",
            first_name="Jane",
            last_name="Smith"
        )
        assert update.username == "newuser"
        assert update.email == "new@example.com"

    def test_username_too_short(self):
        """Test username too short fails"""
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(
                username="ab",
                email="new@example.com",
                first_name="Jane",
                last_name="Smith"
            )
        assert "at least 3 characters" in str(exc_info.value)

    def test_username_invalid_chars(self):
        """Test username with invalid characters fails"""
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(
                username="user@name",
                email="new@example.com",
                first_name="Jane",
                last_name="Smith"
            )
        assert "can only contain" in str(exc_info.value)

    def test_first_name_empty(self):
        """Test empty first name fails"""
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(
                username="newuser",
                email="new@example.com",
                first_name="",
                last_name="Smith"
            )
        assert "cannot be empty" in str(exc_info.value)

    def test_last_name_empty(self):
        """Test empty last name fails"""
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(
                username="newuser",
                email="new@example.com",
                first_name="Jane",
                last_name=""
            )
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_email(self):
        """Test invalid email fails"""
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(
                username="newuser",
                email="not-an-email",
                first_name="Jane",
                last_name="Smith"
            )
        assert "valid email" in str(exc_info.value)