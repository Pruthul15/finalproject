"""End-to-end tests for profile feature using Playwright."""
import pytest
from playwright.async_api import expect

@pytest.mark.asyncio
async def test_profile_page_load_authenticated(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await expect(page.locator("h3:has-text('User Profile')")).to_be_visible()
    await expect(page.locator("text=Profile Information")).to_be_visible()

@pytest.mark.asyncio
async def test_profile_displays_user_info(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    username_display = page.locator("#usernameDisplay")
    await expect(username_display).to_contain_text(test_user_login["username"])

@pytest.mark.asyncio
async def test_edit_profile_form_appears(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await page.click('button:has-text("Edit Profile")')
    await expect(page.locator("#editForm")).to_be_visible()
    await expect(page.locator("#editUsername")).to_be_visible()

@pytest.mark.asyncio
async def test_edit_profile_success(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await page.click('button:has-text("Edit Profile")')
    await page.fill('#editUsername', "updateduser123")
    await page.fill('#editFirstName', "Jane")
    await page.click('button:has-text("Save Changes")')
    await expect(page.locator("#successAlert")).to_be_visible(timeout=5000)
    await expect(page.locator("#successMessage")).not_to_be_empty(timeout=5000)
    await expect(page.locator("#successMessage")).to_contain_text("successfully")

@pytest.mark.asyncio
async def test_edit_profile_cancel(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await page.click('button:has-text("Edit Profile")')
    await page.click('button:has-text("Cancel")')
    await expect(page.locator("#profileSection")).to_be_visible()
    await expect(page.locator("#editForm")).not_to_be_visible()

@pytest.mark.asyncio
async def test_change_password_form_visible(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await expect(page.locator("#passwordForm")).to_be_visible()
    await expect(page.locator('label:has-text("Current Password")')).to_be_visible()

@pytest.mark.asyncio
async def test_change_password_success(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await page.fill('#oldPassword', test_user_login["password"])
    await page.fill('#newPassword', "NewPass@456")
    await page.fill('#confirmPassword', "NewPass@456")
    await page.click('#passwordForm button[type="submit"]')
    await expect(page.locator("#successAlert")).to_be_visible(timeout=5000)
    await expect(page.locator("#successMessage")).not_to_be_empty(timeout=5000)
    await expect(page.locator("#successMessage")).to_contain_text("Password changed successfully")

@pytest.mark.asyncio
async def test_change_password_wrong_old_password(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await page.fill('#oldPassword', "WrongPassword@123")
    await page.fill('#newPassword', "NewPass@456")
    await page.fill('#confirmPassword', "NewPass@456")
    await page.click('#passwordForm button[type="submit"]')
    await expect(page.locator("#errorAlert")).to_be_visible()
    await expect(page.locator("#errorMessage")).to_contain_text("incorrect")

@pytest.mark.asyncio
async def test_change_password_mismatch(page, test_user_login):
    base_url = test_user_login["base_url"]
    await page.goto(f"{base_url}/profile")
    await page.fill('#oldPassword', test_user_login["password"])
    await page.fill('#newPassword', "NewPass@456")
    await page.fill('#confirmPassword', "DifferentPass@789")
    await page.click('#passwordForm button[type="submit"]')
    await expect(page.locator("#errorAlert")).to_be_visible()

@pytest.mark.asyncio
async def test_profile_page_redirect_when_not_logged_in(page, base_url):
    await page.goto(f"{base_url}/profile")
    await page.wait_for_url(f"{base_url}/login")
    assert "/login" in page.url
