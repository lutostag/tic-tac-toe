from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from tictactoe.backend import schemas, crud, models, exceptions
from tictactoe.backend.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/games", response_model=List[schemas.GameOut])
def list_games(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List of all games"""
    return crud.list_games(db, offset=offset, limit=limit)


@app.post("/api/games", response_model=schemas.GameOut)
def create_game(game: schemas.GameIn, db: Session = Depends(get_db)):
    """Create a new game. You can create either a blank new game, or with any
    valid tic-tac-toe game state you would like."""
    return crud.create_game(db=db, game=game)


@app.get("/api/games/{game_id}", response_model=schemas.GameOut)
def get_game(game_id: str, db: Session = Depends(get_db)):
    """View a particular game"""
    game = crud.get_game(db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post("/api/games/{game_id}", response_model=schemas.GameOut)
def update_game(game_id: str, game: schemas.GameIn, db: Session = Depends(get_db)):
    """Update a particular game, must be updated only using valid tic-tac-toe rules.
    Validation of such will be done server-side to prevent cheating clients."""
    try:
        game = crud.update_game(db, game_id=game_id, game=game)
    except exceptions.StateTransitionError as e:
        raise HTTPException(status_code=422, detail=f"Invalid state transition: {e}")
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Tic Tac Toe",
        version="2.5.0",
        description="OpenAPI schema for playing Tic-Tac-Toe",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tic_tac_toe.svg/200px-Tic_tac_toe.svg.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = openapi
