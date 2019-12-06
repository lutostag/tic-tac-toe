from typing import List, Tuple, Union
from pydantic import BaseModel, StrictBool, StrictStr

# type aliases that we can use below for explicit type annotation of models
NullableBoolType = Union[StrictBool, None]
BoardType = List[List[NullableBoolType]]


class GameIn(BaseModel):
    """Game Model - input from client

    If no state is given, it will default to a blank board.

    >>> GameIn(players=['1', '☺'])
    GameIn(players=('1', '☺'), state=[[None, None, None],
                                      [None, None, None],
                                      [None, None, None]])
    >>> GameIn(players=('3', '4'), state=[[True, None, None], \
                                          [None, None, None], \
                                          [None, None, False]])
    GameIn(players=('3', '4'), state=[[True, None, None],
                                      [None, None, None],
                                      [None, None, False]])
    >>> GameIn(players=("3", 5))
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: 1 validation error for GameIn
      ...
    """

    players: Tuple[StrictStr, StrictStr]
    # doing below rather than [[None] * 3] * 3 to avoid the case of references
    # to same row three times
    state: BoardType = [[None] * 3, [None] * 3, [None] * 3]


class GameOut(BaseModel):
    """Game Model - output to client

    All attributes are required
    """

    id: str
    players: Tuple[str, str]
    state: BoardType
