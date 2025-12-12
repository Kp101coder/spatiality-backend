from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import engine, Base, get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, LocationUpdate, LocationResponse
from app.auth import hash_password, verify_password
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Spatiality Backend API",
    description="Backend API for user authentication and location tracking",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Spatiality Backend API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user with hashed password
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/api/users/login", response_model=UserResponse)
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login a user."""
    # Find user by username
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return user


@app.put("/api/users/{user_id}/location", response_model=LocationResponse)
async def update_user_location(
    user_id: int,
    location_data: LocationUpdate,
    db: Session = Depends(get_db)
):
    """Update a user's location."""
    # Find user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update location
    user.last_latitude = location_data.latitude
    user.last_longitude = location_data.longitude
    user.last_location_time = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    return {
        "latitude": user.last_latitude,
        "longitude": user.last_longitude,
        "last_location_time": user.last_location_time
    }


@app.get("/api/users/{user_id}/location", response_model=LocationResponse)
async def get_user_location(user_id: int, db: Session = Depends(get_db)):
    """Get a user's last recorded location."""
    # Find user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "latitude": user.last_latitude,
        "longitude": user.last_longitude,
        "last_location_time": user.last_location_time
    }


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user information by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    debug = os.getenv("APP_DEBUG", "True").lower() == "true"
    
    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
