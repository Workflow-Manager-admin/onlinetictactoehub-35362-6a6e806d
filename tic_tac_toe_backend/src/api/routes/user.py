from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List


router = APIRouter()


class UserProfileResponse(BaseModel):
    username: str
    games_played: int = 0
    games_won: int = 0


class GameHistoryItem(BaseModel):
    game_id: str
    opponent: Optional[str]
    result: str


class GameHistoryResponse(BaseModel):
    games: List[GameHistoryItem]


# PUBLIC_INTERFACE
@router.get("/me", response_model=UserProfileResponse, summary="Get profile of current user")
def get_my_profile():
    """
    Fetch user's profile (mock for now).
    """
    # TODO: Replace with session user & real DB lookup
    return UserProfileResponse(username="demo_user", games_played=0, games_won=0)


# PUBLIC_INTERFACE
@router.get("/history", response_model=GameHistoryResponse, summary="Get user's game history")
def get_game_history():
    """
    Fetch game history for the authenticated user.
    """
    # TODO: Replace with actual lookup
    return GameHistoryResponse(games=[])
