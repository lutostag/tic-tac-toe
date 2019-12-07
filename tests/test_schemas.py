import json
import pytest
from tictactoe.backend.schemas import GameIn
from . import load_fixture
from pydantic.error_wrappers import ValidationError


def test_no_state():
    game = GameIn(players=["one", "two"])
    print(game.dict())
    assert game.dict() == json.loads(load_fixture("games/with_state.json"))


@pytest.mark.parametrize(
    "game",
    [
        load_fixture("games/with_invalid_state.json"),
        load_fixture("games/with_invalid_state_size.json"),
        load_fixture("games/invalid_names.json"),
    ],
)
def test_validation_failure(game):
    with pytest.raises(ValidationError):
        GameIn(**json.loads(game))
