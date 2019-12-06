from typing import List, Tuple, Optional
from pydantic import BaseModel, StrictStr, conint, validator

# type aliases that we can use below for explicit type annotation of models
Null01 = Optional[conint(strict=True, ge=0, le=1)]
BoardType = List[List[Null01]]


class GameIn(BaseModel):
    """Game Model - input from client

    If no state is given, it will default to a blank board.

    >>> GameIn(players=['1', '☺'])
    GameIn(players=('1', '☺'), state=[[None, None, None],
                                      [None, None, None],
                                      [None, None, None]])
    >>> GameIn(players=('3', '4'), state=[[1, None, None], \
                                          [None, None, None], \
                                          [None, None, 0]])
    GameIn(players=('3', '4'), state=[[1, None, None],
                                      [None, None, None],
                                      [None, None, 0]])
    >>> GameIn(players=("3", 5))
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: ...
      ...
    >>> GameIn(players=("0", "1"), state=[[0, 0, 0], [1, 1, 1], [None]])
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: ...
      ...
    """

    players: Tuple[StrictStr, StrictStr]
    # doing below rather than [[None] * 3] * 3 to avoid the case of references
    # to same row three times
    state: BoardType = [[None] * 3, [None] * 3, [None] * 3]

    @validator("state")
    def must_be_3x3(cls, v):
        if len(v) != 3:
            raise ValueError("must have 3 rows")
        if any((len(row) != 3 for row in v)):
            raise ValueError("all rows must contain 3 items")
        return v


class GameOut(BaseModel):
    """Game Model - output to client

    All attributes are required
    """

    id: str
    players: Tuple[str, str]
    state: BoardType
