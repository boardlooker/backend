from sqlalchemy import Boolean, Column, Integer, String, Date, SmallInteger
from sqlalchemy.orm import declarative_base

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
