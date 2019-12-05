from fastapi import FastAPI

app = FastAPI()


@app.get("/api/games")
def read_api_games():
    return []
