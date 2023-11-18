from sqlalchemy import Boolean, Column, Integer, String, Date, SmallInteger, ForeignKey
from sqlalchemy.orm import declarative_base

from database.schemas import BookingStatus

Base = declarative_base()


class BaseModelWithID(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


class User(BaseModelWithID):
    __tablename__ = "users"

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    birthdate = Column(Date)

    is_active = Column(Boolean, nullable=False, default=True)

    def __str__(self) -> str:
        return f"User: {self.username}"


class Boardgame(BaseModelWithID):
    __tablename__ = 'boardgames'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    year = Column(SmallInteger, nullable=False)
    language = Column(SmallInteger, nullable=False)
    genre = Column(SmallInteger, nullable=False)

    def __str__(self) -> str:
        return f"Boardgame: {self.id} {self.title}"


class BoardgameLocation(BaseModelWithID):
    __tablename__ = 'boardgamelocations'

    boardgame_id = Column(ForeignKey('boardgames.id'))
    location_id = Column(Integer, nullable=True)  # TODO: wait for Zarina
    available = Column(Boolean, nullable=False, default=True)

    def __str__(self) -> str:
        return f"BG Location: {self.boardgame_id} {self.location_id}"


class Booking(BaseModelWithID):
    __tablename__ = 'bookings'

    user_id = Column(ForeignKey('users.id'), nullable=False)
    status = Column(SmallInteger, nullable=False, default=BookingStatus.success)
    bg_location_id = Column(ForeignKey('boardgamelocations.id'), nullable=False)
    slot = Column(SmallInteger, nullable=False)
