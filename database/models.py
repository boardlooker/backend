from sqlalchemy import Boolean, Column, Integer, String, Date
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
