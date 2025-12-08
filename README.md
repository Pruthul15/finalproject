# 🎓 Final Project - FastAPI Calculator with User Profile & Password Management

A professional full-stack web application built with **FastAPI** that demonstrates complete mastery of modern web development. Features include user authentication with JWT, secure password management, user profile management, calculator operations (BREAD), comprehensive testing, Docker containerization, and CI/CD automation.

**Status:** ✅ Feature-complete | ✅ 161 Tests Passing | ✅ Production-ready

---

## 📋 Quick Summary

| Aspect | Technology |
|--------|-----------|
| **Backend** | FastAPI + SQLAlchemy ORM |
| **Database** | PostgreSQL |
| **Authentication** | JWT (HS256) + bcrypt password hashing |
| **Frontend** | Jinja2 templates + HTML5/CSS3/JavaScript |
| **Testing** | pytest (unit, integration) + Playwright (E2E) |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions (automated testing & deployment) |
| **Deployment** | Docker Hub |

---

## 🎯 Key Features

### Authentication & Security
- ✅ **User Registration** - Email and username validation with bcrypt password hashing
- ✅ **Secure Login** - JWT token generation (HS256) with refresh tokens
- ✅ **Password Hashing** - Industry-standard bcrypt with salt
- ✅ **Protected Routes** - JWT-based access control
- ✅ **Session Management** - Secure token storage

### User Profile Management (NEW)
- ✅ **View Profile** - Display user information (email, username, name)
- ✅ **Edit Profile** - Update email, username, first name, last name
- ✅ **Password Change** - Secure password change with current password verification
- ✅ **User Isolation** - Users can only access/modify their own data

### Calculator Operations (BREAD)
- ✅ **Browse** - GET /calculations (list all user calculations)
- ✅ **Read** - GET /calculations/{id} (get one calculation)
- ✅ **Add** - POST /calculations (create new calculation)
- ✅ **Edit** - PUT /calculations/{id} (update calculation)
- ✅ **Delete** - DELETE /calculations/{id} (remove calculation)

### Testing & Quality
- ✅ **161 Tests Passing** - Unit, integration, and E2E tests
- ✅ **84% Code Coverage** - Comprehensive test coverage
- ✅ **Playwright E2E Tests** - Browser automation tests
- ✅ **Professional Testing** - All edge cases and error scenarios covered

### Deployment & DevOps
- ✅ **Docker Containerization** - Multi-container setup with PostgreSQL
- ✅ **GitHub Actions CI/CD** - Automated testing and deployment
- ✅ **Docker Hub Deployment** - Automatic image push on test success
- ✅ **Security Scanning** - Trivy vulnerability scanning

---

## 📖 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Using the Web Interface](#using-the-web-interface)
- [Features in Detail](#features-in-detail)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

---

## 🔧 Requirements

- **Python:** 3.10 or higher
- **Docker & Docker Compose:** Latest version
- **Git:** For version control
- **Virtual Environment:** `venv` (included with Python)

---

## 📥 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/Pruthul15/finalproject.git
cd finalproject
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright (for E2E tests)

```bash
python -m playwright install chromium
```

---

## 🚀 Running Locally

### Option 1: SQLite (Quick Start - No Docker Required)

```bash
# Set environment variable for SQLite
export DATABASE_URL="sqlite:///./local_dev.db"

# Start the application
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Access the application:**
- Home: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/register
- Login: http://127.0.0.1:8000/login
- Dashboard: http://127.0.0.1:8000/dashboard
- API Docs: http://127.0.0.1:8000/docs
- Profile: http://127.0.0.1:8000/profile (after login)

### Option 2: PostgreSQL (Local)

```bash
# Install PostgreSQL and create database
createdb fastapi_db

# Set environment variable
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_db"

# Start the application
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🐳 Running with Docker

### Start All Services

```bash
# Build and start containers
docker-compose up -d

# Wait for services to initialize (15 seconds)
sleep 15

# Verify application is running
curl http://localhost:8000/health
# Expected response: {"status":"ok"}
```

### Access Application

- **Home Page:** http://localhost:8000/
- **Register:** http://localhost:8000/register
- **Login:** http://localhost:8000/login
- **Dashboard:** http://localhost:8000/dashboard
- **Profile:** http://localhost:8000/profile
- **API Docs:** http://localhost:8000/docs
- **pgAdmin:** http://localhost:5050 (PostgreSQL management)

### Stop All Services

```bash
docker-compose down
```

### Rebuild and Start

```bash
docker-compose up --build -d
```

---

## 🧪 Running Tests

### Activate Virtual Environment First

```bash
source venv/bin/activate
```

### Run All Tests (Unit + Integration + E2E)

```bash
# Run all tests with coverage report
pytest -v --tb=short

# Expected output: 161 passed
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit -v -q

# Integration tests only
pytest tests/integration -v -q

# E2E tests only (requires app running)
pytest tests/e2e -v -q

# Exclude E2E tests
pytest tests/unit tests/integration -v -q
```

### View Code Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=term-missing --cov-report=html

# Open HTML report in browser
open htmlcov/index.html  # macOS
start htmlcov\index.html # Windows
xdg-open htmlcov/index.html # Linux
```

### Run Tests with Docker (App Already Running)

```bash
# Terminal 1: Start the application
docker-compose up

# Terminal 2: Run tests
docker-compose exec web pytest tests/ -v -q
```

---

## 🔌 API Endpoints

### Authentication Endpoints

#### Register New User
```bash
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePass@123"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true
}
```

#### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass@123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_at": "2025-12-09T12:30:00Z"
}
```

### Profile Endpoints

#### Get User Profile
```bash
GET /api/profile
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Update User Profile
```bash
PUT /api/profile
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "username": "johndoe",
  "email": "newemail@example.com",
  "first_name": "Jonathan",
  "last_name": "Doe"
}
```

**Response (200 OK):**
```json
{
  "username": "johndoe",
  "email": "newemail@example.com",
  "first_name": "Jonathan",
  "last_name": "Doe"
}
```

#### Change Password
```bash
POST /api/change-password
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "current_password": "SecurePass@123",
  "new_password": "NewSecurePass@456",
  "confirm_password": "NewSecurePass@456"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

### Calculator Endpoints (BREAD)

#### Browse - Get All Calculations
```bash
GET /calculations
Authorization: Bearer {access_token}
```

#### Read - Get One Calculation
```bash
GET /calculations/{calc_id}
Authorization: Bearer {access_token}
```

#### Add - Create Calculation
```bash
POST /calculations
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "operation": "addition",
  "operand1": 10,
  "operand2": 5
}
```

#### Edit - Update Calculation
```bash
PUT /calculations/{calc_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "operation": "subtraction",
  "operand1": 20,
  "operand2": 3
}
```

#### Delete - Remove Calculation
```bash
DELETE /calculations/{calc_id}
Authorization: Bearer {access_token}
```

---

## 🌐 Using the Web Interface

### Register

1. Navigate to http://localhost:8000/register
2. Fill in the registration form:
   - **Username** - Unique identifier (alphanumeric)
   - **Email** - Valid email address (must be unique)
   - **First Name** - Your first name
   - **Last Name** - Your last name
   - **Password** - Must contain: uppercase, lowercase, digit, special char, 8+ chars
3. Click "Register"
4. On success, redirected to login page

**Password Requirements:**
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one digit (0-9)
- ✅ At least one special character (!@#$%^&*)

### Login

1. Navigate to http://localhost:8000/login
2. Enter your username and password
3. Click "Sign in"
4. JWT token automatically stored in browser localStorage
5. Redirected to dashboard

### Dashboard

After login, you can:
1. **Create Calculations**
   - Select operation (Addition, Subtraction, Multiplication, Division)
   - Enter operands
   - Click "Calculate"
2. **View Calculations** - All your calculations displayed in table
3. **View Details** - Click "View" to see detailed calculation
4. **Edit Calculation** - Click "Edit" to modify operands/operation
5. **Delete Calculation** - Click "Delete" to remove
6. **Logout** - Click "Logout" to exit

### Profile (NEW FEATURE)

1. Navigate to http://localhost:8000/profile (after login)
2. **View Profile** - See current information
3. **Edit Profile** - Update email, username, first/last name
4. **Change Password** - Click "Change Password"
   - Enter current password
   - Enter new password (meets requirements above)
   - Confirm new password
   - Click "Change Password"
5. **Verify** - Old password no longer works, new password active immediately

---

## 💎 Features in Detail

### User Profile & Password Management

**What was built:**
- User profile page (`/profile`) showing user information
- Edit profile form allowing updates to email, username, first/last name
- Password change form with current password verification
- Backend validation and database persistence
- User isolation (users can only access their own data)

**Security measures:**
- Passwords hashed with bcrypt (never stored in plain text)
- Current password verified before allowing password change
- Email and username must be unique
- All endpoints secured with JWT authentication
- Database constraints enforce data integrity

**Testing:**
- Unit tests for password hashing logic
- Integration tests for profile endpoints
- E2E tests for complete workflows (positive and negative scenarios)
- Tests verify data persistence and authorization

### Calculator (BREAD Operations)

**Implemented operations:**
- Addition, Subtraction, Multiplication, Division
- Each calculation stored with: operation type, operands, result, timestamp, user

**Features:**
- All calculations tied to logged-in user
- Full BREAD support (Browse, Read, Add, Edit, Delete)
- Calculations persist in PostgreSQL database
- Real-time recalculation on edit

---

## 📁 Project Structure

```
finalproject/
├── app/
│   ├── auth/                    # Authentication logic
│   │   ├── dependencies.py      # JWT dependency injection
│   │   ├── jwt.py              # JWT token operations
│   │   └── redis.py            # Token blacklisting
│   │
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py             # User model + auth methods
│   │   └── calculation.py       # Calculation model
│   │
│   ├── schemas/                 # Pydantic data validation
│   │   ├── base.py             # Base schemas
│   │   ├── user.py             # User-related schemas
│   │   ├── calculation.py       # Calculation schemas
│   │   └── token.py            # Token schemas
│   │
│   ├── core/
│   │   └── config.py           # Configuration & settings
│   │
│   ├── main.py                 # FastAPI application & routes
│   ├── database.py             # Database connection
│   └── database_init.py        # Table initialization
│
├── templates/
│   ├── base.html               # Base template
│   ├── index.html              # Home page
│   ├── register.html           # Registration form
│   ├── login.html              # Login form
│   ├── dashboard.html          # Dashboard (calculations)
│   └── profile.html            # Profile (NEW FEATURE)
│
├── static/
│   └── css/
│       └── style.css           # Styling
│
├── tests/
│   ├── unit/                   # Unit tests
│   │   ├── test_calculator.py
│   │   └── test_password_validation.py
│   ├── integration/            # Integration tests
│   │   ├── test_profile_routes.py
│   │   ├── test_user.py
│   │   ├── test_calculation.py
│   │   ├── test_user_auth.py
│   │   └── ...
│   ├── e2e/                    # End-to-end tests
│   │   ├── test_profile_e2e.py (NEW FEATURE TESTS)
│   │   └── test_fastapi_calculator.py
│   └── conftest.py             # Pytest configuration
│
├── .github/
│   └── workflows/
│       ├── test.yml            # Run tests
│       ├── deploy.yml          # Docker build & push
│       ├── security.yml        # Security scanning
│       └── notify.yml          # Status notifications
│
├── docker-compose.yml          # Multi-container orchestration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment variables (local)
└── README.md                   # This file
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization
- **Passlib + bcrypt** - Password hashing
- **PyJWT** - JWT token generation/validation

### Frontend
- **Jinja2** - Template engine
- **HTML5** - Semantic markup
- **CSS3** - Styling
- **JavaScript** - Client-side interactivity

### Database
- **PostgreSQL** - Relational database
- **SQLite** - Local development database

### Testing
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **pytest-asyncio** - Async test support
- **Playwright** - Browser automation (E2E)

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD automation
- **Trivy** - Container security scanning
- **Docker Hub** - Container registry

---

## ⚙️ CI/CD Pipeline

### GitHub Actions Workflow

Automated pipeline runs on every push:

#### 1. **Test Job** (~2 min)
- Install dependencies
- Run all 161 tests
- Generate coverage report (84%)
- Upload results

#### 2. **Security Job** (~2 min)
- Build Docker image
- Scan with Trivy
- Identify vulnerabilities

#### 3. **Deploy Job** (~3 min)
- Login to Docker Hub
- Push image with tags:
  - `latest` (most recent)
  - `<git-sha>` (specific commit)
- Update Docker Hub repo

#### 4. **Notify Job** (~1 min)
- Summarize pipeline status
- Report success/failure

**View workflows:** https://github.com/Pruthul15/finalproject/actions

### Deployment to Docker Hub

```bash
# Pull latest image
docker pull pruthul123/finalproject:latest

# Run image
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  pruthul123/finalproject:latest
```

**Docker Hub Repository:** https://hub.docker.com/r/pruthul123/finalproject

---

## 🔒 Security Features

- ✅ **Password Hashing** - bcrypt with cryptographic salt
- ✅ **JWT Authentication** - HS256 algorithm with expiration
- ✅ **CORS Protection** - Properly configured cross-origin requests
- ✅ **SQL Injection Prevention** - SQLAlchemy parameterized queries
- ✅ **User Isolation** - Users only access their own data
- ✅ **Token Expiration** - Automatic token refresh/expiration
- ✅ **HTTP Security Headers** - Secure cookie settings
- ✅ **Input Validation** - Pydantic schema validation on all inputs

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
```

### Database Connection Error

```bash
# For PostgreSQL
createdb fastapi_db

# For Docker
docker-compose down -v
docker-compose up -d
sleep 15
```

### Tests Failing

```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run tests
pytest -v --tb=short
```

### Playwright Tests Not Running

```bash
# Install Playwright browsers
python -m playwright install chromium

# Ensure app is running on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Run E2E tests
pytest tests/e2e -v
```

### Docker Build Fails

```bash
# Clean up Docker
docker system prune -a

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Test Coverage

**Current Coverage: 84%**

| Module | Coverage | Status |
|--------|----------|--------|
| app/__init__.py | 100% | ✅ |
| app/auth/dependencies.py | 93% | ✅ |
| app/core/config.py | 100% | ✅ |
| app/models/user.py | 90% | ✅ |
| app/models/calculation.py | 92% | ✅ |
| app/schemas/user.py | 93% | ✅ |
| app/schemas/calculation.py | 92% | ✅ |
| **TOTAL** | **84%** | **✅** |

**Test Breakdown:**
- 27 Unit Tests
- 87 Integration Tests
- 47 E2E Tests
- **Total: 161 Tests Passing**

---

## 📝 Environment Variables

Create `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Security
BCRYPT_ROUNDS=12

# PostgreSQL (Docker)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_db
```

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/Pruthul15/finalproject |
| **Docker Hub Image** | https://hub.docker.com/r/pruthul123/finalproject |
| **GitHub Actions** | https://github.com/Pruthul15/finalproject/actions |
| **API Documentation** | http://localhost:8000/docs (when running) |
| **Coverage Report** | `htmlcov/index.html` (after running tests) |

---

## 👤 Author

- **Name:** Pruthul Patel
- **Email:** pp8787140@gmail.com
- **GitHub:** https://github.com/Pruthul15
- **Docker Hub:** https://hub.docker.com/u/pruthul123

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎓 Course Information

**Course:** IS601 - Web Systems Development  
**Institution:** New Jersey Institute of Technology (NJIT)  
**Instructor:** Prof. Thomas Licciardello  
**Final Project:** User Profile & Password Change Feature  

---

