"""End-to-end tests for profile feature using Playwright."""
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_profile_page_load_authenticated(page, test_user_login):
    """Test loading profile page while authenticated"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Verify profile page loaded
    await expect(page.locator("h3:has-text('User Profile')")).to_be_visible()
    await expect(page.locator("text=Profile Information")).to_be_visible()


@pytest.mark.asyncio
async def test_profile_displays_user_info(page, test_user_login):
    """Test that profile page displays correct user information"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Verify user info is displayed
    username_display = page.locator("#usernameDisplay")
    await expect(username_display).to_contain_text(test_user_login["username"])


@pytest.mark.asyncio
async def test_edit_profile_form_appears(page, test_user_login):
    """Test that edit profile form appears when edit button is clicked"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Click edit button
    await page.click('button:has-text("Edit Profile")')
    
    # Verify edit form appears
    await expect(page.locator("#editForm")).to_be_visible()
    await expect(page.locator("#editUsername")).to_be_visible()


@pytest.mark.asyncio
async def test_edit_profile_success(page, test_user_login):
    """Test successfully editing profile"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Click edit button
    await page.click('button:has-text("Edit Profile")')
    
    # Update fields
    await page.fill('#editUsername', "updateduser123")
    await page.fill('#editFirstName', "Jane")
    
    # Submit form
    await page.click('button:has-text("Save Changes")')
    
    # Verify success message appears
    await expect(page.locator("#successAlert")).to_be_visible()
    await expect(page.locator("#successMessage")).to_contain_text("successfully")


@pytest.mark.asyncio
async def test_edit_profile_cancel(page, test_user_login):
    """Test canceling edit profile"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Click edit button
    await page.click('button:has-text("Edit Profile")')
    
    # Click cancel button
    await page.click('button:has-text("Cancel")')
    
    # Verify edit form is hidden and profile section is visible
    await expect(page.locator("#profileSection")).to_be_visible()
    await expect(page.locator("#editForm")).not_to_be_visible()


@pytest.mark.asyncio
async def test_change_password_form_visible(page, test_user_login):
    """Test that password change form is visible"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Verify password form is visible
    await expect(page.locator("#passwordForm")).to_be_visible()
    await expect(page.locator('label:has-text("Current Password")')).to_be_visible()


@pytest.mark.asyncio
async def test_change_password_success(page, test_user_login):
    """Test successfully changing password"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Fill password change form
    await page.fill('#oldPassword', test_user_login["password"])
    await page.fill('#newPassword', "NewPass@456")
    await page.fill('#confirmPassword', "NewPass@456")
    
    # Submit form
    await page.click('#passwordForm button[type="submit"]')
    
    # Verify success message appears
    await expect(page.locator("#successAlert")).to_be_visible()
    await expect(page.locator("#successMessage")).to_contain_text("Password changed successfully")


@pytest.mark.asyncio
async def test_change_password_wrong_old_password(page, test_user_login):
    """Test changing password with wrong old password shows error"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Fill password change form with wrong old password
    await page.fill('#oldPassword', "WrongPassword@123")
    await page.fill('#newPassword', "NewPass@456")
    await page.fill('#confirmPassword', "NewPass@456")
    
    # Submit form
    await page.click('#passwordForm button[type="submit"]')
    
    # Verify error message appears
    await expect(page.locator("#errorAlert")).to_be_visible()
    await expect(page.locator("#errorMessage")).to_contain_text("incorrect")


@pytest.mark.asyncio
async def test_change_password_mismatch(page, test_user_login):
    """Test changing password when passwords don't match shows error"""
    base_url = test_user_login["base_url"]
    
    # Navigate to profile page
    await page.goto(f"{base_url}/profile")
    
    # Fill password change form with mismatched passwords
    await page.fill('#oldPassword', test_user_login["password"])
    await page.fill('#newPassword', "NewPass@456")
    await page.fill('#confirmPassword', "DifferentPass@789")
    
    # Submit form
    await page.click('#passwordForm button[type="submit"]')
    
    # Verify error message appears
    await expect(page.locator("#errorAlert")).to_be_visible()


@pytest.mark.asyncio
async def test_profile_page_redirect_when_not_logged_in(page, base_url):
    """Test that unauthenticated users are redirected from profile page"""
    # Navigate to profile page without logging in
    await page.goto(f"{base_url}/profile")
    
    # Should be redirected to login page
    await page.wait_for_url(f"{base_url}/login")
    assert "/login" in page.url