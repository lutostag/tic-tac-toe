import json
import pytest
from tictactoe.schemas import GameIn
from . import load_fixture
from pydantic.error_wrappers import ValidationError


def test_no_state():
    game = GameIn(players=["one", "two"])
    assert game.players == ("one", "two")
    assert len(game.state) == 3


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
