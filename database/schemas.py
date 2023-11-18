import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        strict=False,
        populate_by_name=True,
    )


class UserRetrieve(Schema):
    username: str
    full_name: str
    password: str
    birthdate: datetime.date


class BoardgameLanguage(int, Enum):
    russian = 1
    english = 2


class BoardgameGenre(int, Enum):
    other = 0

    cards = 1
    quest = 2
    fantasy = 3
    realism = 4
    logic = 5
    fielded = 6


class BoardgameBase(Schema):
    title: str
    description: str
    year: int = Field(gt=1900, lt=2025)
    language: BoardgameLanguage | None = BoardgameLanguage.russian
    genre: BoardgameGenre | None = BoardgameGenre.other


class BookingStatus(int, Enum):
    success = 1
    canceled = 2
