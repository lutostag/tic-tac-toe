from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from tictactoe import schemas, crud, models
from tictactoe.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/games", response_model=List[schemas.GameOut])
def list_games(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_games(db, offset=offset, limit=limit)


@app.post("/api/games", response_model=schemas.GameOut)
def create_game(game: schemas.GameIn, db: Session = Depends(get_db)):
    return crud.create_game(db=db, game=game)


@app.get("/api/games/{game_id}", response_model=schemas.GameOut)
def get_game(game_id: str, db: Session = Depends(get_db)):
    game = crud.get_game(db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post("/api/games/{game_id}", response_model=schemas.GameOut)
def update_game(game_id: str, game: schemas.GameIn, db: Session = Depends(get_db)):
    game = crud.update_game(db, game_id=game_id, game=game)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game
