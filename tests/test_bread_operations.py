"""Test suite for BREAD operations and authentication."""
import pytest
from uuid import uuid4


class TestUserAuthentication:
    """Test user registration and login."""
    
    def test_register_user_success(self, client, fake_user_data):
        """Test successful registration."""
        response = client.post(
            "/auth/register",
            json={
                **fake_user_data,
                "confirm_password": fake_user_data["password"]
            }
        )
        
        assert response.status_code in [200, 201], f"Got {response.status_code}: {response.json()}"
        data = response.json()
        assert "id" in data or "username" in data
    
    def test_register_user_duplicate_email(self, client):
        """Test duplicate email registration fails."""
        email = f"duplicate_{uuid4().hex[:8]}@example.com"
        
        user_data = {
            "username": f"user_{uuid4().hex[:8]}",
            "email": email,
            "password": "Password@123",
            "confirm_password": "Password@123",
            "first_name": "User",
            "last_name": "One"
        }
        
        response1 = client.post("/auth/register", json=user_data)
        assert response1.status_code in [200, 201]
        
        # Try to register with same email but different username
        user_data["username"] = f"user_{uuid4().hex[:8]}"
        response2 = client.post("/auth/register", json=user_data)
        assert response2.status_code in [400, 409, 422]
    
    def test_login_user_success(self, client, fake_user_data):
        """Test successful login."""
        client.post(
            "/auth/register",
            json={
                **fake_user_data,
                "confirm_password": fake_user_data["password"]
            }
        )
        
        response = client.post(
            "/auth/login",
            json={
                "username": fake_user_data["username"],
                "password": fake_user_data["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data or "token" in data
    
    def test_login_user_wrong_password(self, client, fake_user_data):
        """Test login with wrong password fails."""
        client.post(
            "/auth/register",
            json={
                **fake_user_data,
                "confirm_password": fake_user_data["password"]
            }
        )
        
        response = client.post(
            "/auth/login",
            json={
                "username": fake_user_data["username"],
                "password": "WrongPassword@123"
            }
        )
        assert response.status_code == 401


class TestBREADOperations:
    """Test BREAD operations for calculations."""
    
    def test_add_calculation_success(self, client, auth_headers):
        """Test CREATE calculation."""
        response = client.post(
            "/calculations",
            json={"type": "addition", "inputs": [5, 3]},
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data.get("result") == 8
    
    def test_browse_calculations(self, client, auth_headers):
        """Test READ/BROWSE calculations."""
        for i in range(2):
            client.post(
                "/calculations",
                json={"type": "addition", "inputs": [i, i+1]},
                headers=auth_headers
            )
        
        response = client.get(
            "/calculations",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_browse_calculations_pagination(self, client, auth_headers):
        """Test browse with pagination."""
        response = client.get(
            "/calculations?skip=0&limit=10",
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_read_calculation_success(self, client, auth_headers):
        """Test READ calculation."""
        create_resp = client.post(
            "/calculations",
            json={"type": "multiplication", "inputs": [4, 5]},
            headers=auth_headers
        )
        
        calc_id = create_resp.json().get("id")
        
        response = client.get(
            f"/calculations/{calc_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("result") == 20
    
    def test_read_calculation_not_found(self, client, auth_headers):
        """Test reading non-existent calculation."""
        fake_id = str(uuid4())
        response = client.get(
            f"/calculations/{fake_id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_read_calculation_invalid_id_format(self, client, auth_headers):
        """Test reading with invalid ID."""
        response = client.get(
            "/calculations/invalid-id",
            headers=auth_headers
        )
        assert response.status_code == 400
    
    def test_edit_calculation_success(self, client, auth_headers):
        """Test UPDATE calculation."""
        create_resp = client.post(
            "/calculations",
            json={"type": "subtraction", "inputs": [10, 3]},
            headers=auth_headers
        )
        
        calc_id = create_resp.json().get("id")
        
        response = client.put(
            f"/calculations/{calc_id}",
            json={"inputs": [10, 5]},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("result") == 5
    
    def test_edit_calculation_not_found(self, client, auth_headers):
        """Test updating non-existent calculation."""
        fake_id = str(uuid4())
        response = client.put(
            f"/calculations/{fake_id}",
            json={"inputs": [1, 1]},
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_delete_calculation_success(self, client, auth_headers):
        """Test DELETE calculation."""
        create_resp = client.post(
            "/calculations",
            json={"type": "addition", "inputs": [1, 1]},
            headers=auth_headers
        )
        
        calc_id = create_resp.json().get("id")
        
        response = client.delete(
            f"/calculations/{calc_id}",
            headers=auth_headers
        )
        
        assert response.status_code in [200, 204]
        
        get_resp = client.get(
            f"/calculations/{calc_id}",
            headers=auth_headers
        )
        
        assert get_resp.status_code == 404
    
    def test_delete_calculation_not_found(self, client, auth_headers):
        """Test deleting non-existent calculation."""
        fake_id = str(uuid4())
        response = client.delete(
            f"/calculations/{fake_id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_delete_calculation_unauthorized(self, client, fake_user_data):
        """Test authorization for delete."""
        # User 1 creates calculation
        user1_data = fake_user_data
        client.post(
            "/auth/register",
            json={
                **user1_data,
                "confirm_password": user1_data["password"]
            }
        )
        login1 = client.post(
            "/auth/login",
            json={
                "username": user1_data["username"],
                "password": user1_data["password"]
            }
        )
        token1 = login1.json().get("access_token") or login1.json().get("token")
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        create_resp = client.post(
            "/calculations",
            json={"type": "addition", "inputs": [1, 1]},
            headers=headers1
        )
        calc_id = create_resp.json().get("id")
        
        # User 2 tries to delete
        user2_data = {
            "username": f"user_{uuid4().hex[:8]}",
            "email": f"user_{uuid4().hex[:8]}@example.com",
            "password": "Pass@123",
            "first_name": "User",
            "last_name": "Two"
        }
        client.post(
            "/auth/register",
            json={
                **user2_data,
                "confirm_password": user2_data["password"]
            }
        )
        login2 = client.post(
            "/auth/login",
            json={
                "username": user2_data["username"],
                "password": user2_data["password"]
            }
        )
        token2 = login2.json().get("access_token") or login2.json().get("token")
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        response = client.delete(f"/calculations/{calc_id}", headers=headers2)
        assert response.status_code in [403, 404]


class TestCalculationOperations:
    """Test calculation operations."""
    
    def test_add_operation(self, client, auth_headers):
        """Test addition."""
        response = client.post(
            "/calculations",
            json={"type": "addition", "inputs": [5, 3]},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json().get("result") == 8
    
    def test_subtract_operation(self, client, auth_headers):
        """Test subtraction."""
        response = client.post(
            "/calculations",
            json={"type": "subtraction", "inputs": [10, 3]},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json().get("result") == 7
    
    def test_multiply_operation(self, client, auth_headers):
        """Test multiplication."""
        response = client.post(
            "/calculations",
            json={"type": "multiplication", "inputs": [4, 5]},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json().get("result") == 20
    
    def test_divide_operation(self, client, auth_headers):
        """Test division."""
        response = client.post(
            "/calculations",
            json={"type": "division", "inputs": [20, 4]},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json().get("result") == 5.0
    
    def test_divide_by_zero(self, client, auth_headers):
        """Test division by zero."""
        response = client.post(
            "/calculations",
            json={"type": "division", "inputs": [5, 0]},
            headers=auth_headers
        )
        assert response.status_code in [400, 422]
    
    def test_invalid_operation(self, client, auth_headers):
        """Test invalid operation."""
        response = client.post(
            "/calculations",
            json={"type": "invalid_op", "inputs": [5, 3]},
            headers=auth_headers
        )
        assert response.status_code in [400, 422]


class TestErrorHandling:
    """Test error handling."""
    
    def test_missing_required_fields(self, client, auth_headers):
        """Test missing fields."""
        response = client.post(
            "/calculations",
            json={"type": "addition"},
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_invalid_input_types(self, client, auth_headers):
        """Test invalid types."""
        response = client.post(
            "/calculations",
            json={"type": "addition", "inputs": ["string", 3]},
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_empty_inputs_array(self, client, auth_headers):
        """Test empty inputs."""
        response = client.post(
            "/calculations",
            json={"type": "addition", "inputs": []},
            headers=auth_headers
        )
        assert response.status_code in [400, 422]
    
    def test_invalid_token(self, client):
        """Test invalid token."""
        headers = {"Authorization": "Bearer invalid_token_xyz"}
        response = client.get("/calculations", headers=headers)
        assert response.status_code == 401
    
    def test_no_token(self, client):
        """Test no token."""
        response = client.get("/calculations")
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])