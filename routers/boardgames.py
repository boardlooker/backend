from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Boardgame, BoardgameLocation
from database.schemas import BoardgameBase, BoardgameRetrieve
from database.session import StartedSession
from utils.dependencies import CurrentUser

router = APIRouter(prefix="/boardgames", tags=["boardgames"])


@router.get("/{loc_id}/")
async def boardgames_by_location(loc_id: int):
    """Список настольных игр которые есть в конкретной локации."""


@router.get("/{bg_id}")
async def get_boardgame_by_id(bg_id: int):
    """Получить данные конкретной настольной игры по ее id."""


@router.post("/", response_model=BoardgameRetrieve)
async def create_new_boardgame(
    game: BoardgameBase,
    session: Session = Depends(StartedSession),
):
    """Создать настолку в таблице."""
    bg = Boardgame(
        **game.model_dump(),
    )
    session.add(bg)
    session.commit()
    return bg


@router.get("/", response_model=list[BoardgameRetrieve])
async def fetch_all_boardgames_ever_possible(
    session: Session = Depends(StartedSession),
):
    """Получить список всех доступных настольных игр."""
    return session.scalars(select(Boardgame)).all()


@router.post('/connect')
async def connect_boardgame_to_loc(
    bg_id: int, loc_id: int,
    available: bool = True,
):
    """Привязать настолку к локации. 
    Available по умолчанию True, если хотите скрыть из общего списка сделайте False."""
    try:
        BoardgameLocation.insert(
            boardgame_id=bg_id,
            location_id=loc_id,
            available=True,
        )
    except:
        raise HTTPException(status_code=404, detail='Not found')


@router.post("/{bg_id}")
async def make_a_booking(
    user: CurrentUser,
    bg_id: int,
    slot_id: int = Body(..., ge=1, le=24, description="Номер слота от 1 до 24 (слот = 1 час времени)"),
):
    """Создать заявку на бронирование настольной игры."""
