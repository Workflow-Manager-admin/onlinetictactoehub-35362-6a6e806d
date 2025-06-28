from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers (to be extended in actual implementation)
from .routes.auth import router as auth_router
from .routes.game import router as game_router
from .routes.user import router as user_router

# Tags metadata for automatic API docs grouping
openapi_tags = [
    {
        "name": "auth",
        "description": (
            "Operations related to user registration, login, and authentication."
        ),
    },
    {
        "name": "game",
        "description": (
            "Endpoints for creating, joining, and playing Tic Tac Toe games."
        ),
    },
    {
        "name": "user",
        "description": "User profile, stats, and history endpoints.",
    },
]

# PUBLIC_INTERFACE
app = FastAPI(
    title="Tic Tac Toe Backend API",
    description=(
        "REST API backend for the Tic Tac Toe online game. Handles authentication, "
        "gameplay, and user operations."
    ),
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for separation of features
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(game_router, prefix="/game", tags=["game"])
app.include_router(user_router, prefix="/user", tags=["user"])


@app.get("/", tags=["meta"])
def health_check():
    """
    PUBLIC_INTERFACE
    Health check endpoint for server readiness.
    """
    return {"message": "Healthy"}


# To extend: add background jobs, websocket support, etc.
# in new files/modules under src/api or src/core
