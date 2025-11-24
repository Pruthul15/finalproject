# Final Project — FastAPI Calculator with Profile & Password Change

This repository is the Final Project for the course. It is a FastAPI application that implements a calculator service with user authentication (JWT), profile management (view/update), and password change functionality. The project includes unit, integration, and Playwright E2E tests, Docker support, and a CI pipeline (GitHub Actions) scaffold.

---

**Status:** feature-complete for user profile & password-change. Tests included (unit, integration, e2e).

## Quick summary
- Backend: FastAPI + SQLAlchemy
- Auth: JWT (access + refresh), bcrypt password hashing (Passlib)
- Frontend: Jinja2 templates (profile page includes edit & change-password forms)
- Tests: pytest (unit & integration) + Playwright (E2E)
- Container: Docker + docker-compose

---

## Requirements
- Python 3.10+ (project uses a virtual environment)
- `venv` (standard Python venv)
- Docker & Docker Compose (for container runs)

Files of interest:
- `app/main.py` - application routes (web + API)
- `app/models/user.py` - User model, hashing, authentication helpers
- `app/schemas/user.py` - Pydantic schemas for profile and password change
- `templates/profile.html` - Profile page with edit & change-password UI
- `tests/` - unit, integration, and e2e test suites

---

## Setup (local, recommended)
Follow these steps to run the app and tests locally using `python3` and a `venv`.

1. Create and activate venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. (Optional) Install Playwright browsers for E2E tests

```bash
python -m playwright install chromium
```

---

## Run the application locally (development)
By default the app tries to use the `DATABASE_URL` from `app/core/config.py`. For quick local runs and for tests you can use a local SQLite DB by overriding the env var.

```bash
# Use sqlite for quick local run (no Postgres required)
export DATABASE_URL="sqlite:///./local_dev.db"
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

After startup the app will create tables automatically. Open:

- Home: http://127.0.0.1:8001/
- Profile page: http://127.0.0.1:8001/profile
- API docs (when running): http://127.0.0.1:8001/docs

The profile page expects an `access_token` in `localStorage` (the E2E tests set this automatically after creating a test user).

---

## Tests

Run tests from the project root with your venv active.

1) Unit + Integration tests

```bash
python -m pytest tests/unit tests/integration -q
```

2) E2E (Playwright) tests

Start the application first (use sqlite override shown above), then run:

```bash
# Ensure Playwright browsers are installed
python -m playwright install chromium

# Run E2E profile tests
python -m pytest tests/e2e/test_profile_e2e.py -q
```

Notes:
- E2E fixtures assume the app listens on `http://localhost:8001` (see `tests/conftest.py`).
- The E2E fixture `test_user_login` registers a test user via the API and sets `access_token` into the browser `localStorage`.

---

## Feature details (what was added/verified for this final project)

- User Profile page (`/profile`): view username, email, first/last name.
- Edit profile: client-side form (template `templates/profile.html`) and backend `PUT /api/profile` which:
  - validates uniqueness of username/email
  - updates `username`, `email`, `first_name`, `last_name`
- Password change: form on profile page and backend route `POST /api/change-password` which:
  - verifies the current password
  - validates and hashes the new password
  - updates `user.password`
- Tests:
  - Unit tests for calculation & auth logic
  - Integration tests for DB interactions and API routes
  - Playwright E2E tests covering profile view, edit, and password-change flows (positive and negative scenarios)

---

## Docker (quick)

Build and run with `docker-compose` (the repo includes `docker-compose.yml`):

```bash
docker-compose up --build -d
# wait for DB to initialize (15s)
docker-compose logs -f web
```

If you only want to build the image locally:

```bash
docker build -t finalproject:local .
docker run -e DATABASE_URL="sqlite:///./local.db" -p 8001:8001 finalproject:local
```

---

## CI / CD (notes)

- The repository contains a GitHub Actions workflow scaffold to run tests and build Docker images. CI should:
  - install dependencies
  - run unit + integration tests
  - start the app or required services and run E2E tests (Playwright)
  - build Docker image and push to Docker Hub if tests pass

I can scaffold or refine the `.github/workflows` files if you want CI to run Playwright E2E on GitHub-hosted runners (requires installing browsers and starting the app in the workflow).

---

## How you can proceed (options)

- I can add/update a GitHub Actions workflow that runs the test matrix and builds/pushes Docker image. (CI/CD)
- I can add Alembic migrations if you plan to change models in the future.
- I can add a short developer `Makefile` or `scripts/` to simplify common commands (start, test, e2e).

Tell me which one you want and I'll implement it.

---

## Contact / Author

- Project owner: Pruthul Patel
- Repo path: workspace root

---

License: MIT
# Assignment 13: JWT Authentication & CI/CD Pipeline

## 📋 Project Overview

This project implements a complete JWT-based authentication system for a FastAPI calculator application. It includes user registration/login, secure password hashing, front-end forms with client-side validation, comprehensive E2E tests, and a full CI/CD pipeline with Docker and GitHub Actions.

## 🎯 Key Features

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **User Registration** - Email and username validation with password hashing
- ✅ **User Login** - Credential verification and JWT token generation
- ✅ **Front-End Pages** - HTML forms for registration, login, and dashboard
- ✅ **Protected Routes** - Dashboard accessible only to authenticated users
- ✅ **Playwright E2E Tests** - Comprehensive browser automation tests
- ✅ **CI/CD Pipeline** - Automated testing and Docker Hub deployment
- ✅ **Code Coverage** - 66%+ coverage with unit and integration tests

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Pruthul15/assignment13.git
cd assignment13

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🐳 Running with Docker

### Start the Application

```bash
# Build and start all containers
docker-compose up -d

# Wait for services to start (about 15 seconds)
sleep 15

# Verify app is running
curl http://localhost:8000/health
```

### Access the Application

- **Home Page:** http://localhost:8000/
- **Register:** http://localhost:8000/register
- **Login:** http://localhost:8000/login
- **Dashboard:** http://localhost:8000/dashboard (requires login)
- **API Docs:** http://localhost:8000/docs
- **pgAdmin:** http://localhost:5050

### Stop the Application

```bash
docker-compose down
```

## 🧪 Running Tests

### Activate Virtual Environment

```bash
source venv/bin/activate
```

### Run All Tests

```bash
# Run all tests with coverage
pytest -v --tb=short

# Expected: 99 PASSED
```

### Run Only E2E Tests

```bash
# Run Playwright E2E tests
pytest tests/e2e/ -v --tb=short
```

### Run Only Unit Tests

```bash
# Run unit tests
pytest tests/unit/ -v --tb=short
```

### Run Only Integration Tests

```bash
# Run integration tests
pytest tests/integration/ -v --tb=short
```

### View Coverage Report

```bash
# Generate and display coverage report
pytest --cov=app --cov-report=term-missing

# Open HTML coverage report
open htmlcov/index.html
```

## 🔐 API Endpoints

### Authentication

#### Register New User
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePass@123",
  "confirm_password": "SecurePass@123"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "username": "newuser",
  "email": "user@example.com",
  "is_active": true
}
```

#### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "username": "newuser",
  "password": "SecurePass@123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_at": "2025-11-05T04:26:11Z"
}
```

## 🧑‍💻 Using the Web Interface

### Register a New User

1. Go to http://localhost:8000/register
2. Fill in the form:
   - Username
   - Email (valid format required)
   - First Name
   - Last Name
   - Password (8+ chars, uppercase, lowercase, digit, special char)
   - Confirm Password
3. Click Register
4. On success, redirects to login page

### Login

1. Go to http://localhost:8000/login
2. Enter username and password
3. Click Login
4. On success, redirects to dashboard with JWT token stored in localStorage

### Dashboard

1. After login, you're on the dashboard
2. Can create calculations:
   - Select operation type (Addition, Subtraction, etc.)
   - Enter numbers
   - Click Calculate
3. View calculation history
4. Delete calculations
5. Click Logout to exit

## 🔑 Password Requirements

Passwords must contain:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter
- ✅ At least one lowercase letter
- ✅ At least one digit
- ✅ At least one special character (!@#$%^&*, etc.)

## 📊 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL |
| **Frontend** | Jinja2, HTML5, CSS3, JavaScript |
| **Authentication** | JWT (HS256), bcrypt |
| **Testing** | pytest, Playwright, pytest-cov |
| **DevOps** | Docker, Docker Compose, GitHub Actions |
| **Cache** | Redis |

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The pipeline automatically runs on every push to main branch:

1. **Test Job** (runs in ~5 min)
   - Spins up PostgreSQL and Redis containers
   - Runs all 99 tests
   - Calculates code coverage
   - Uploads coverage report

2. **Security Job** (runs in ~2 min)
   - Builds Docker image
   - Scans with Trivy for vulnerabilities
   - Uploads results

3. **Deploy Job** (runs in ~3 min)
   - Logs into Docker Hub
   - Pushes image with `latest` and git SHA tags
   - Updates Docker Hub repository

4. **Notify Job** (runs in ~1 min)
   - Summarizes pipeline status

**View workflows:** https://github.com/Pruthul15/assignment13/actions

## 🐳 Docker Hub

Docker image is automatically pushed to:
- **Repository:** https://hub.docker.com/r/pruthul123/assignment13
- **Tags:**
  - `latest` - Most recent build
  - `<git-sha>` - Specific commit version

### Pull and Run Image

```bash
# Pull the image
docker pull pruthul123/assignment13:latest

# Run the image
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET_KEY="your-secret-key" \
  pruthul123/assignment13:latest
```

## 📁 Project Structure

```
assignment13/
├── app/
│   ├── auth/              # Authentication logic
│   │   ├── jwt.py        # JWT token generation
│   │   ├── dependencies.py # Auth dependencies
│   │   └── redis.py      # Token blacklisting
│   ├── models/
│   │   ├── user.py       # User model with auth methods
│   │   └── calculation.py # Calculation models (polymorphic)
│   ├── schemas/
│   │   ├── user.py       # Pydantic user schemas
│   │   ├── token.py      # Token schemas
│   │   └── calculation.py # Calculation schemas
│   ├── core/
│   │   └── config.py     # Configuration
│   ├── database.py       # Database setup
│   ├── database_init.py  # Table initialization
│   └── main.py           # FastAPI app
├── templates/
│   ├── register.html     # Registration page
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard (protected)
│   ├── layout.html       # Base template
│   └── index.html        # Home page
├── static/
│   └── css/
│       └── style.css     # Styling
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/      # Integration tests
│   ├── e2e/             # End-to-end tests
│   └── conftest.py      # Pytest configuration
├── .github/
│   └── workflows/
│       └── test.yml     # GitHub Actions workflow
├── docker-compose.yml    # Multi-container setup
├── Dockerfile           # Docker image
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🧹 Database Initialization

Tables are automatically created on application startup:

```bash
# Manual initialization (if needed)
docker-compose exec web python -m app.database_init
```

## 🔒 Security Features

- ✅ **Password Hashing** - bcrypt with salt
- ✅ **JWT Tokens** - HS256 algorithm with 30-min expiration
- ✅ **CORS** - Properly configured for cross-origin requests
- ✅ **SQL Injection Prevention** - SQLAlchemy parameterized queries
- ✅ **Token Blacklisting** - Redis-backed token invalidation
- ✅ **Protected Routes** - Dependency injection for auth checks

## 🐛 Troubleshooting

### Port Already in Use

If port 5432 or 8000 is already in use:

```bash
# Change Docker port (edit docker-compose.yml)
sed -i 's/5432:5432/5433:5432/g' docker-compose.yml
sed -i 's/:5432/:5433/g' app/core/config.py

# Then restart
docker-compose down && docker-compose up -d
```

### Database Connection Error

```bash
# Reinitialize database
docker-compose exec web python -m app.database_init

# Or restart all containers
docker-compose restart
```

### Tests Failing

```bash
# Clean up and restart
docker-compose down -v
docker-compose up -d
sleep 15
pytest -v --tb=short
```

## 📝 Environment Variables

Create a `.env` file for local development:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/fastapi_db
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key
ALGORITHM=HS256
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_db
```

## 🎯 Assignment Requirements Met

### 1. JWT Authentication ✅
- ✅ `/register` endpoint validates and stores users
- ✅ `/login` endpoint authenticates and returns JWT
- ✅ Pydantic validation on all inputs
- ✅ Password hashing with bcrypt

### 2. Front-End Integration ✅
- ✅ Register page with HTML form
- ✅ Login page with HTML form
- ✅ Dashboard page (protected)
- ✅ Client-side validation
- ✅ JWT stored in localStorage

### 3. Playwright E2E Tests ✅
- ✅ Positive tests: Registration & login success
- ✅ Negative tests: Invalid input handling
- ✅ All 12 E2E tests passing

### 4. CI/CD Pipeline ✅
- ✅ GitHub Actions workflow configured
- ✅ All 99 tests pass automatically
- ✅ Docker image pushed to Docker Hub
- ✅ Security scanning with Trivy

### 5. Documentation ✅
- ✅ README with full instructions
- ✅ REFLECTION.md with experiences
- ✅ Inline code comments
- ✅ API endpoint documentation

## 👤 Author

- **Name:** Pruthul Patel
- **GitHub:** https://github.com/Pruthul15
- **Docker Hub:** https://hub.docker.com/u/pruthul123

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Links

- **GitHub Repository:** https://github.com/Pruthul15/assignment13
- **Docker Hub Repository:** https://hub.docker.com/r/pruthul123/assignment13
- **GitHub Actions:** https://github.com/Pruthul15/assignment13/actions
- **API Documentation:** http://localhost:8000/docs (when running locally)

---

