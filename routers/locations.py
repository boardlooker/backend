import datetime
from enum import Enum
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.session import StartedSession
from database.models import Location
from database.schemas import LocationRetrieve, LocationType

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[LocationRetrieve])
async def get_locations_filtered(
    city: str | None = None,
    name_regex: str | None = None,
    loc_type: LocationType | None = None,
    session: Session = Depends(StartedSession),
):
    """Получение всех локаций-партнеров по фильтру или без него."""
    if city is None:
        city = "%%"
    if loc_type is None:
        loc_type = "%%"
    if name_regex is None:
        name_regex = ""
    return list(
        Location.filter(
            Location.title.like(f"%{name_regex}%"),
            Location.location_city.like(city),
            Location.location_type.like(loc_type),
        )
    )


@router.get("/{id}", response_model=LocationRetrieve)
async def get_location_by_id(id: int):
    """Получение информации о конкретной локации по ее id."""
    if location := Location.single(Location.id == id):
        return location
    raise HTTPException(status_code=404, detail="Локация не найдена")


class LocationCreate(BaseModel):
    title: str
    location: str
    location_city: str
    location_address: str
    location_type: LocationType = LocationType.other


@router.get("/{loc_id}/bookings")
async def get_location_bookings_for_date(
    loc_id: int,
    day: datetime.date,
    session: Session = Depends(StartedSession),
):
    """Получение списка забронированных слотов на выбранный день по выбранной локации."""


@router.post("/", response_model=LocationRetrieve)
async def create_new_location(data: LocationCreate):
    return Location.insert(**data.model_dump())
