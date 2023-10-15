from typing import Annotated

from fastapi import Depends, Header


async def authorized_user(token: str = Header(...)) -> object:
    ...


CurrentUser = Annotated[object, Depends(authorized_user)]
