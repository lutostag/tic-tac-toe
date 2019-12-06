from sqlalchemy.orm import Session
from tictactoe import models, schemas


def get_game(db: Session, game_id: str):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def create_game(db: Session, game: schemas.GameIn):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(db: Session, game_id: str, game: schemas.GameIn):
    db_game = db.query(models.Game).filter(models.Game.id == game_id)
    db_game.update(game.dict())
    db.commit()
    return db_game.first()


def list_games(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Game).offset(offset).limit(limit).all()
