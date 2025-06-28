# Tic Tac Toe Backend (FastAPI)

This is the backend service for the online Tic Tac Toe application.

## Structure

- `src/api/main.py`: FastAPI app instance, middleware, and route registration.
- `src/api/routes/`: Auth, game, and user feature routers (extensible).
- In-memory store is used for demo; update to use a real database for production.
- Swagger/OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Features

- User registration & authentication (`/auth`)
- Create, join, and play Tic Tac Toe games (`/game`)
- Get user profile and game history (`/user`)

## Running Locally

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

## Extension

- Replace in-memory stores with database models (see TODO in code).
- Implement JWT authentication with dependency in routers.
- Add win/draw logic in `game.py` moves.
- Add REST endpoints for additional features as needed.
- Update CORS settings for production.

## For Contributors

- Extend routers in `src/api/routes/` with accurate Pydantic models, docstrings, and comments.
- Follow file structure and example endpoints for new features.
