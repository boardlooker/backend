import datetime
from enum import Enum

from fastapi import APIRouter


router = APIRouter(prefix='/locations', tags=['Locations'])


class LocationType(str, Enum):
    bar = 'bar'
    cafe = 'cafe'
    hookah = 'hookah'


@router.get('/')
async def get_locations_filtered(
    city: str | None,
    name_regex: str | None,
    loc_type: LocationType | None,
):
    """Получение всех локаций-партнеров по фильтру или без него."""


@router.get('/{id}')
async def get_location_by_id(id: int):
    """Получение информации о конкретной локации по ее id."""


@router.get('/{loc_id}/bookings')
async def get_location_bookings_for_date(loc_id: int, day: datetime.date):
    """Получение списка забронированных слотов на выбранный день по выбранной локации."""
