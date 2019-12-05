import requests
import os

SERVER = os.environ.get("TICTACTOE_SERVER", "http://localhost:8000")


def test_get_games():
    assert requests.get(SERVER + "/api/games").status_code == 200


def test_create_game():
    json = {
        "players": ["one", "two"],
    }
    response = requests.post(SERVER + "/api/games", json=json)
    assert response.status_code == 200
