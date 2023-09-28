from __future__ import annotations

from typing import List

from pydantic import BaseModel, PositiveInt


class TokenDataSchema(BaseModel):
    username: str | None = None


class LoginSchema(BaseModel):
    username: str
    password: str


class GroupProfileSchema(BaseModel):
    class Config:
        orm_mode = True

    id: PositiveInt
    name: str


class PermissionsSchema(BaseModel):
    read_users: bool
    modify_users: bool
    grant_permissions: bool
    revoke_permissions: bool
    read_threats: bool
    modify_threats: bool


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    id: PositiveInt
    email: str
    first_name: str
    last_name: str
    disabled: bool = True
    profile_image: str | None = None
    permissions: PermissionsSchema
    groups: List[GroupProfileSchema]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserSchema


class UserCreateSchema(BaseModel):
    class Config:
        orm_mode = True

    email: str
    password: str
    first_name: str
    last_name: str


class EmailConfirmationSchema(BaseModel):
    key: str


class RequestPasswordResetSchema(BaseModel):
    email: str


class PasswordResetSchema(BaseModel):
    key: str
    new_password: str
