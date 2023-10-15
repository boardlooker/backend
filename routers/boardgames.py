from fastapi import APIRouter
from pydantic import Field

from utils.dependencies import CurrentUser

router = APIRouter(prefix='/boardgames', tags=['boardgames'])


@router.get('/{loc_id}/')
async def boardgames_by_location(loc_id: int):
    """Список настольных игр которые есть в конкретной локации."""


@router.get('/{bg_id}')
async def get_boardgame_by_id(bg_id: int):
    """Получить данные конкретной настольной игры по ее id."""


@router.post('/{bg_id}')
async def make_a_booking(
    user: CurrentUser,
    bg_id: int,
    slot_id: int = Field(ge=1, le=24, description='Номер слота от 1 до 24 (слот = 1 час времени)')
):
    """Создать заявку на бронирование настольной игры."""