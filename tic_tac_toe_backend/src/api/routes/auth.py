from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


router = APIRouter()


# PUBLIC_INTERFACE
class UserRegisterRequest(BaseModel):
    username: str = Field(..., description="Desired username")
    password: str = Field(..., min_length=6, description="User password, min 6 chars")


class UserLoginRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class AuthResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = "bearer"


# Simple memory store placeholder
users_db = {}


# PUBLIC_INTERFACE
@router.post("/register", response_model=AuthResponse, summary="Register a new user")
def register(user: UserRegisterRequest):
    """
    Registers a new user.
    """
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    # Store user in memory (replace with DB in real impl)
    users_db[user.username] = user.password
    return AuthResponse(access_token="dummy_token", token_type="bearer")


# PUBLIC_INTERFACE
@router.post("/login", response_model=AuthResponse, summary="Authenticate a user and get JWT token")
def login(user: UserLoginRequest):
    """
    Authenticates and returns an access token.
    """
    if users_db.get(user.username) != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return AuthResponse(access_token="dummy_token", token_type="bearer")
