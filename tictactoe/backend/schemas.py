import itertools
from collections import Counter
from uuid import UUID
from typing import List, Tuple, Optional
from pydantic import BaseModel, Field, StrictStr, conint, validator
from tictactoe.backend.exceptions import StateTransitionError

# type aliases that we can use below for explicit type annotation of models
Null01 = Optional[conint(strict=True, ge=0, le=1)]
BoardType = List[List[Null01]]

PLAYERS_DESC = "A list of strings representing the players in the game. \
    Will start with the first player to join, then when the second joins the \
    list will have two items. The state can only be changed after both players \
    have entered the game."
BOARD_STATE_DESC = "A 3x3 matrix (nested lists) with representations: \
    null=empty, 0=taken by the first player (x), 1=taken by the second player (o)"


def blank_state():
    """Returns a blank board (3x3) matrix filled with None"""
    # cannot use [[None] * 3] * 3 to avoid multiple references to same row
    return [[None] * 3, [None] * 3, [None] * 3]


class GameIn(BaseModel):
    """Game Model - input from client

    If no state is given, it will default to a blank board.
    """

    players: List[StrictStr] = Field(
        ...,
        min_items=1,
        max_items=2,
        title="The players in this game",
        description=PLAYERS_DESC,
    )
    state: BoardType = Field(
        blank_state(),
        max_items=3,
        min_items=3,
        title="The state of the board",
        description=BOARD_STATE_DESC,
    )

    def must_be_3x3(cls, value):
        """validates board size"""
        if len(value) != 3:
            raise ValueError("must have 3 rows")
        if any((len(row) != 3 for row in value)):
            raise ValueError("all rows must contain 3 items")
        return value

    @validator("state")
    def must_have_fair_coverage(cls, value):
        flat = list(itertools.chain.from_iterable(value))
        counter = Counter(flat)
        if not 0 <= counter[0] - counter[1] <= 1:
            raise ValueError(
                "player turn order is incorrect, \
                    please start with player 1, and alternate turns"
            )
        return value

    @validator("players")
    def all_entered_before_starting(cls, value, values):
        if len(value) == 1 and "state" in values and values["state"] != blank_state():
            raise ValueError("all players must enter before starting the game")
        return value

    def validate_move(self, prev):
        """validates this move is valid given the previous GameIn."""
        if (
            len(prev.players) == 2
            and prev.players != self.players
            or self.players[0] != prev.players[0]
        ):
            raise StateTransitionError("players cannot change in the middle of a game")

        self_flat = list(itertools.chain.from_iterable(self.state))
        prev_flat = list(itertools.chain.from_iterable(prev.state))
        different = [
            (new, old) for (new, old) in zip(self_flat, prev_flat) if new != old
        ]

        if len(different) > 1:
            raise StateTransitionError("more than one space changed")

        for (_, old) in different:
            if old is not None:
                raise StateTransitionError("reusing an already claimed space")


class GameOut(GameIn):
    """Game Model - output to client

    All attributes are required
    """

    state: BoardType = Field(
        ...,
        max_items=3,
        min_items=3,
        title="The state of the board",
        description=BOARD_STATE_DESC,
    )
    id: UUID = Field(..., title="Unique ID of this game")

    class Config:
        orm_mode = True
