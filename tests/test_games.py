import requests
import os

SERVER = os.environ.get('TICTACTOE_SERVER', "http://localhost:8000")

def test_get_games():
    assert requests.get(SERVER + '/api/games').status_code == 200
