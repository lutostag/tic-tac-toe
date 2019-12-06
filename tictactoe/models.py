from uuid import uuid4
from sqlalchemy import Column, JSON
from sqlalchemy_utils import UUIDType
from tictactoe.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    players = Column(JSON)
    state = Column(JSON)
