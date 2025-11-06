import logging
from typing import Generator, Dict, List
from contextlib import contextmanager

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db, get_engine, get_sessionmaker
from app.models.user import User

# ======================================================================================
# Logging Configuration
# ======================================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ======================================================================================
# Database Configuration - USE SQLITE FOR TESTS
# ======================================================================================
fake = Faker()
Faker.seed(12345)

TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = get_engine(database_url=TEST_DATABASE_URL)
TestingSessionLocal = get_sessionmaker(engine=test_engine)

# ======================================================================================
# Helper Functions
# ======================================================================================
def create_fake_user() -> Dict[str, str]:
    """Generate fake user data."""
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "username": fake.unique.user_name(),
        "password": "TestPass@123"
    }

@contextmanager
def managed_db_session():
    """Context manager for safe database session handling."""
    session = TestingSessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

# ======================================================================================
# Database Fixtures
# ======================================================================================
@pytest.fixture(scope="session", autouse=True)
def setup_test_database(request):
    """Set up test database before all tests."""
    logger.info("Creating tables...")
    try:
        Base.metadata.create_all(bind=test_engine)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error setting up test database: {str(e)}")
        raise

    yield  # Tests run here

    if not request.config.getoption("--preserve-db", default=False):
        logger.info("Dropping test database tables...")
        try:
            Base.metadata.drop_all(bind=test_engine)
        except Exception as e:
            logger.warning(f"Error dropping tables: {e}")

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Provide test database session."""
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# ======================================================================================
# FastAPI Client Fixture
# ======================================================================================
@pytest.fixture
def client(db_session: Session):
    """Provide TestClient for FastAPI app."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

# ======================================================================================
# Test Data Fixtures
# ======================================================================================
@pytest.fixture
def fake_user_data() -> Dict[str, str]:
    """Provide fake user data."""
    return create_fake_user()

@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create test user in database."""
    user_data = create_fake_user()
    user = User.register(db_session, user_data)
    db_session.commit()
    db_session.refresh(user)
    logger.info(f"Created test user ID: {user.id}")
    return user

@pytest.fixture
def seed_users(db_session: Session, request) -> List[User]:
    """Seed multiple test users."""
    num_users = getattr(request, "param", 5)
    users = []
    for _ in range(num_users):
        user_data = create_fake_user()
        user = User.register(db_session, user_data)
        users.append(user)
    
    db_session.commit()
    logger.info(f"Seeded {len(users)} users.")
    return users

@pytest.fixture
def auth_headers(client: TestClient) -> Dict[str, str]:
    """Create authenticated user and return headers."""
    user_data = create_fake_user()
    
    # Register
    reg_response = client.post(
        "/auth/register",
        json={
            **user_data,
            "confirm_password": user_data["password"]
        }
    )
    
    if reg_response.status_code not in [200, 201]:
        pytest.skip(f"Registration failed: {reg_response.json()}")
    
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"Login failed: {login_response.json()}")
    
    token = login_response.json().get("access_token") or login_response.json().get("token")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_user_data() -> Dict[str, str]:
    """Provide test user data."""
    return create_fake_user()

# ======================================================================================
# E2E/Playwright Fixtures - PORT 8001
# ======================================================================================
@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for async tests."""
    import asyncio
    if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    return None


@pytest_asyncio.fixture
async def page():
    """Provide Playwright browser page for E2E tests."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        pytest.skip("Playwright not installed")
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()


@pytest.fixture(scope="session")
def fastapi_server():
    """Provide FastAPI test server URL - PORT 8001."""
    return "http://localhost:8001"


@pytest.fixture(scope="session")
def base_url(fastapi_server: str) -> str:
    """Provide base URL for E2E tests."""
    return fastapi_server


@pytest_asyncio.fixture
async def test_user_login(client: TestClient, base_url: str):
    """Create user and return login info for E2E tests."""
    user_data = create_fake_user()
    
    # Register
    reg_response = client.post(
        "/auth/register",
        json={
            **user_data,
            "confirm_password": user_data["password"]
        }
    )
    
    if reg_response.status_code not in [200, 201]:
        pytest.skip(f"Registration failed: {reg_response.json()}")
    
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )
    
    if login_response.status_code != 200:
        pytest.skip(f"Login failed: {login_response.json()}")
    
    token = login_response.json().get("access_token")
    
    return {
        "username": user_data["username"],
        "password": user_data["password"],
        "email": user_data["email"],
        "token": token,
        "base_url": base_url
    }

# ======================================================================================
# Pytest Options
# ======================================================================================
def pytest_addoption(parser):
    """Add custom options."""
    parser.addoption("--preserve-db", action="store_true", help="Keep test database")
    parser.addoption("--run-slow", action="store_true", help="Run slow tests")

def pytest_collection_modifyitems(config, items):
    """Skip slow tests unless --run-slow."""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="use --run-slow")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

# ======================================================================================
# Pytest Hooks
# ======================================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results for debugging."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        logger.error(f"Test failed: {item.name}")
        if rep.longrepr:
            logger.error(f"Error: {rep.longrepr}")

# ======================================================================================
# Markers for Test Organization
# ======================================================================================
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "asyncio: marks tests as async"
    )