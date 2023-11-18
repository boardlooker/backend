import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User
from database.schemas import UserRetrieve, Schema
from database.session import StartedSession
from utils.dependencies import CurrentUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", tags=["Auth"])
async def get_my_profile_data(user: CurrentUser):
    """Получение данных профиля по токену."""
    return user


class SignUpData(BaseModel):
    username: str
    password: str
    full_name: str
    birthdate: datetime.date


@router.post("/signup", tags=["Auth"], response_model=UserRetrieve)
async def create_new_user(data: SignUpData, session=Depends(StartedSession)):
    """Регистрация нового пользователя."""
    user = User(
        username=data.username,
        full_name=data.full_name,
        password=data.password,
        birthdate=data.birthdate,
        is_active=True,
    )
    session.add(user)
    session.commit()
    return user


class Token(Schema):
    token: str


@router.post("/signin", tags=["Auth"], response_model=Token)
async def sign_in_for_token(
    username: str,
    password: str,
    session: Session = Depends(StartedSession),
):
    """Вход в учетную запись для получения токена."""
    user = session.scalar(select(User).where(User.username == username, User.password == password))
    if user is not None:
        return Token(token=f"{username}_{password}")
    raise HTTPException(status_code=403, detail="Неправильный логин или пароль")


@router.get("/{id}")
async def get_user_by_id(id: int):
    """Получение данных пользователя по его ID."""
    ...
