# Spatiality Backend

FastAPI backend for the Spatiality Project with MySQL/MariaDB database support.

## Features

- User registration and authentication
- Password hashing with bcrypt
- Location tracking (latitude, longitude, timestamp)
- RESTful API endpoints
- MySQL/MariaDB database integration

## Project Structure

```
spatiality-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # Database configuration and connection
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic schemas for request/response
│   └── auth.py          # Password hashing utilities
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- MySQL or MariaDB server

### 2. Clone the Repository

```bash
git clone https://github.com/Kp101coder/spatiality-backend.git
cd spatiality-backend
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

1. Create a database in MySQL/MariaDB:
```sql
CREATE DATABASE spatiality_db;
```

2. Copy `.env.example` to `.env` and update with your database credentials:
```bash
cp .env.example .env
```

3. Edit `.env` file:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=spatiality_db
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=True
```

### 5. Run the Application

```bash
python -m app.main
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /` - Check API status

### User Management
- `POST /api/users/register` - Register a new user
  ```json
  {
    "username": "john_doe",
    "password": "secure_password"
  }
  ```

- `POST /api/users/login` - Login user
  ```json
  {
    "username": "john_doe",
    "password": "secure_password"
  }
  ```

- `GET /api/users/{user_id}` - Get user information

### Location Tracking
- `PUT /api/users/{user_id}/location` - Update user location
  ```json
  {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
  ```

- `GET /api/users/{user_id}/location` - Get user's last location

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| username | VARCHAR(255) | Unique username |
| password | VARCHAR(255) | Hashed password |
| last_latitude | FLOAT | Last recorded latitude |
| last_longitude | FLOAT | Last recorded longitude |
| last_location_time | DATETIME | Timestamp of last location update |
| created_at | DATETIME | User creation timestamp |
| updated_at | DATETIME | Last update timestamp |

## Security

- Passwords are hashed using bcrypt
- Environment variables for sensitive configuration
- Input validation using Pydantic schemas

## Technologies Used

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **PyMySQL** - MySQL/MariaDB driver
- **Pydantic** - Data validation
- **Passlib** - Password hashing
- **Uvicorn** - ASGI server
