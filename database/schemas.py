import datetime

from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        strict=False,
        populate_by_name=True,
    )


class UserRetrieve(Schema):
    username: str
    full_name: str
    password: str
    birthdate: datetime.date
