from typing import List

from pydantic import BaseModel, PositiveInt


class UserProfileSchema(BaseModel):
    id: PositiveInt
    email: str


class GroupSchema(BaseModel):
    id: PositiveInt
    name: str
    users: List[UserProfileSchema]
