from sqlalchemy.orm import Session
from tictactoe.backend import models, schemas


def get_game(db: Session, game_id: str):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def create_game(db: Session, game: schemas.GameIn):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(db: Session, game_id: str, game: schemas.GameIn):
    db_game = get_game(db, game_id)
    if db_game is None:
        return None
    current = schemas.GameOut.from_orm(db_game)
    game.validate_move(current)
    db_game.players = game.players
    db_game.state = game.state
    db.commit()
    db.refresh(db_game)
    return db_game


def list_games(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Game).offset(offset).limit(limit).all()
