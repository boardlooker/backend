from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User
from database.session import StartedSession


async def authorized_user(token: str = Header(...), session: Session = Depends(StartedSession)) -> object:
    exc = HTTPException(status_code=403, detail='Ошибка при декодировании токена')
    try:
        username, password = token.split('_')
    except:
        raise exc
    if user := session.scalar(
        select(User).where(
            User.username == username, User.password == password
        )
    ):
        return user
    raise exc


CurrentUser = Annotated[User, Depends(authorized_user)]
