from uuid import UUID
from typing import List, Tuple, Optional
from pydantic import BaseModel, StrictStr, conint, validator

# type aliases that we can use below for explicit type annotation of models
Null01 = Optional[conint(strict=True, ge=0, le=1)]
BoardType = List[List[Null01]]


class GameIn(BaseModel):
    """Game Model - input from client

    If no state is given, it will default to a blank board.

    """

    players: Tuple[StrictStr, StrictStr]
    # doing below rather than [[None] * 3] * 3 to avoid the case of references
    # to same row three times
    state: BoardType = [[None, None, None], [None, None, None], [None, None, None]]

    @validator("state")
    def must_be_3x3(cls, value):
        if len(value) != 3:
            raise ValueError("must have 3 rows")
        if any((len(row) != 3 for row in value)):
            raise ValueError("all rows must contain 3 items")
        return value


class GameOut(GameIn):
    """Game Model - output to client

    All attributes are required
    """

    state: BoardType
    id: UUID

    class Config:
        orm_mode = True
