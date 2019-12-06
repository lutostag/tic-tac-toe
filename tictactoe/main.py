from fastapi import FastAPI
from tictactoe.schemas import GameIn


app = FastAPI()


@app.get("/api/games")
def read_api_games():
    return []


@app.post("/api/games")
def post_api_games(game: GameIn):
    return game
