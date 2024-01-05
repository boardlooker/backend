from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Boardgame, BoardgameLocation
from database.schemas import BoardgameBase, BoardgameRetrieve
from database.session import StartedSession
from utils.dependencies import CurrentUser

router = APIRouter(prefix="/boardgames", tags=["boardgames"])


@router.get("/{loc_id}/", response_model=list[BoardgameRetrieve])
async def boardgames_by_location(loc_id: int):
    """Список настольных игр которые есть в конкретной локации."""
    bg_locs = BoardgameLocation.select(BoardgameLocation.location_id == loc_id)
    result = []
    for bg_loc in bg_locs:
        boardgame = Boardgame.single(Boardgame.id == bg_loc.boardgame_id)
        if not boardgame:
            print(f'Empty BG_ID in {bg_loc.id}. Skipped.')
            continue
        result.append(boardgame)
    return result


@router.get("/{bg_id}", response_model=BoardgameRetrieve)
async def get_boardgame_by_id(bg_id: int):
    """Получить данные конкретной настольной игры по ее id."""
    if bg := Boardgame.single(Boardgame.id == bg_id):
        return bg
    raise HTTPException(status_code=404, detail='Game is not found')


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
        if BoardgameLocation.single(
            BoardgameLocation.boardgame_id == bg_id,
            BoardgameLocation.location_id == loc_id,
        ) is not None:
            raise ValueError
        BoardgameLocation.insert(
            boardgame_id=bg_id,
            location_id=loc_id,
            available=True,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='Not found or relation exists')


@router.post("/{bg_id}")
async def make_a_booking(
    user: CurrentUser,
    bg_id: int,
    slot_id: int = Body(..., ge=1, le=24, description="Номер слота от 1 до 24 (слот = 1 час времени)"),
):
    """Создать заявку на бронирование настольной игры."""
