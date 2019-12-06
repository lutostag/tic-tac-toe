import requests
import os
import pytest

SERVER = os.environ.get("TICTACTOE_SERVER", "http://localhost:8000")


def load_fixture(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "fixtures", path), "r") as fd:
        return fd.read()


def test_get_games():
    assert requests.get(SERVER + "/api/games").status_code == 200


@pytest.mark.parametrize(
    "json,status",
    [
        (load_fixture("games/without_state.json"), 200),
        (load_fixture("games/with_state.json"), 200),
        (load_fixture("games/with_invalid_state.json"), 422),
        (load_fixture("games/invalid_json.txt"), 400),
    ],
)
def test_create_game(json, status):
    response = requests.post(SERVER + "/api/games", data=json)
    assert response.status_code == status
