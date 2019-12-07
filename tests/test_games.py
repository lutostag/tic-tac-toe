import requests
import os
import pytest
import json
from . import load_fixture

SERVER = os.environ.get("TICTACTOE_SERVER", "http://localhost:8000")


def test_get_games():
    r = requests.get(SERVER + "/api/games")
    assert r.status_code == 200


@pytest.mark.parametrize(
    "json,status",
    [
        (load_fixture("games/without_state.json"), 200),
        (load_fixture("games/with_state.json"), 200),
        (load_fixture("games/with_utf8_players.json"), 200),
        (load_fixture("games/with_invalid_state.json"), 422),
        (load_fixture("games/with_invalid_state_size.json"), 422),
        (load_fixture("games/invalid_json.txt"), 400),
    ],
)
def test_create_game(json, status):
    response = requests.post(SERVER + "/api/games", data=json)
    assert response.status_code == status


def test_create_and_get_then_modify_and_get_game():
    initial = load_fixture("games/without_state.json")

    create_data = requests.post(f"{SERVER}/api/games", data=initial).json()
    uuid = create_data["id"]
    get_data = requests.get(f"{SERVER}/api/games/{uuid}").json()
    assert create_data == get_data


def test_create_and_update_game():
    initial = load_fixture("games/without_state.json")
    updated = load_fixture("games/with_state.json")

    initial_data = requests.post(f"{SERVER}/api/games", data=initial).json()
    uuid = initial_data["id"]
    updated_data = requests.post(f"{SERVER}/api/games/{uuid}", data=updated).json()
    get_data = requests.get(f"{SERVER}/api/games/{uuid}").json()
    assert updated_data == get_data
    assert uuid == updated_data["id"] == get_data["id"]


def test_openapi_works():
    r = requests.get(f"{SERVER}/openapi.json")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_full_game():
    moves = json.loads(load_fixture("games/full_play.json"))
    initial_data = requests.post(f"{SERVER}/api/games", json=moves[0]).json()
    uuid = initial_data["id"]
    for move in moves[1:]:
        r = requests.post(f"{SERVER}/api/games/{uuid}", json=move)
        assert r.status_code == 200
        r = requests.get(f"{SERVER}/api/games/{uuid}")
        assert r.status_code == 200
        if "state" in move:
            assert r.json()["state"] == move["state"]


def test_invalid_transitions():
    moves = json.loads(load_fixture("games/invalid_transitions.json"))
    initial_data = requests.post(f"{SERVER}/api/games", json=moves[0]).json()
    uuid = initial_data["id"]
    for move in moves[1:]:
        r = requests.post(f"{SERVER}/api/games/{uuid}", json=move)
        assert r.status_code == 422
        r = requests.get(f"{SERVER}/api/games/{uuid}")
        assert r.json() == initial_data
