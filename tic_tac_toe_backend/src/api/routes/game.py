from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List


router = APIRouter()


# Placeholder memory store
games_db = {}


class GameCreateRequest(BaseModel):
    player_x: str = Field(..., description="Username of the user starting the game")


class GameJoinRequest(BaseModel):
    game_id: str = Field(..., description="ID of the game to join")
    player_o: str = Field(..., description="Username of the user joining as O")


class GameMoveRequest(BaseModel):
    game_id: str = Field(..., description="ID of the game")
    player: str = Field(..., description="Player making the move ('X' or 'O')")
    position: int = Field(..., ge=0, le=8, description="Board position 0-8")


class GameStateResponse(BaseModel):
    game_id: str
    board: List[Optional[str]] = Field(..., description="Current board state, indexed 0-8")
    next_player: str = Field(..., description="Which player moves next")
    winner: Optional[str] = Field(None, description="Winner if there is one")
    is_draw: bool = Field(False, description="Is the game a draw")


# PUBLIC_INTERFACE
@router.post("/create", response_model=GameStateResponse, summary="Create new Tic Tac Toe game")
def create_game(request: GameCreateRequest):
    """
    Start a new game as X.
    """
    import uuid
    game_id = str(uuid.uuid4())
    games_db[game_id] = {
        "board": [None] * 9,
        "players": {"X": request.player_x, "O": None},
        "next_player": "X",
        "winner": None,
        "is_draw": False,
    }
    return GameStateResponse(
        game_id=game_id,
        board=games_db[game_id]["board"],
        next_player="X",
        winner=None,
        is_draw=False,
    )


# PUBLIC_INTERFACE
@router.post("/join", response_model=GameStateResponse, summary="Join an existing game as O")
def join_game(request: GameJoinRequest):
    """
    Join an existing game as O.
    """
    game = games_db.get(request.game_id)
    if not game or game["players"]["O"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found or already full"
        )
    game["players"]["O"] = request.player_o
    return GameStateResponse(
        game_id=request.game_id,
        board=game["board"],
        next_player=game["next_player"],
        winner=game["winner"],
        is_draw=game["is_draw"],
    )


# PUBLIC_INTERFACE
@router.post("/move", response_model=GameStateResponse, summary="Make a move")
def make_move(request: GameMoveRequest):
    """
    Play a move in a Tic Tac Toe game.
    """
    game = games_db.get(request.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    player_mark = "X" if request.player == game["players"]["X"] else "O"
    if game["board"][request.position] is not None:
        raise HTTPException(status_code=400, detail="Cell already taken")
    if game["winner"] or game["is_draw"]:
        raise HTTPException(status_code=400, detail="Game already finished")
    game["board"][request.position] = player_mark
    # Win logic (simplified for now)...
    # [Place actual win/draw logic here.]
    game["next_player"] = "O" if game["next_player"] == "X" else "X"
    return GameStateResponse(
        game_id=request.game_id,
        board=game["board"],
        next_player=game["next_player"],
        winner=game["winner"],
        is_draw=game["is_draw"],
    )


# PUBLIC_INTERFACE
@router.get("/{game_id}", response_model=GameStateResponse, summary="Get current state of a game")
def get_game_state(game_id: str):
    """
    Get the current board state of a game.
    """
    game = games_db.get(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return GameStateResponse(
        game_id=game_id,
        board=game["board"],
        next_player=game["next_player"],
        winner=game["winner"],
        is_draw=game["is_draw"],
    )
