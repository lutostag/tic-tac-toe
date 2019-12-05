from fastapi import FastAPI
from typing import Tuple
from pydantic import BaseModel

app = FastAPI()


class Game(BaseModel):
    players: Tuple[str, str]


@app.get("/api/games")
def read_api_games():
    return []


@app.post("/api/games")
def post_api_games(game: Game):
    return game
