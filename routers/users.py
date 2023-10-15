import datetime

from fastapi import APIRouter, Header
from pydantic import BaseModel

from utils.dependencies import CurrentUser

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', tags=['Auth'])
async def get_my_profile_data(user: CurrentUser):
    """Получение данных профиля по токену."""
    return user


class SignUpData(BaseModel):
    username: str
    password: str
    full_name: str
    birthdate: datetime.date


@router.post('/signup', tags=['Auth'])
async def create_new_user(data: SignUpData):
    """Регистрация нового пользователя."""
    ...


@router.post('/signin', tags=['Auth'])
async def sign_in_for_token(username: str, password: str):
    """Вход в учетную запись для получения токена."""
    ...


@router.get('/{id}')
async def get_user_by_id(id: int):
    """Получение данных пользователя по его ID."""
    ...
