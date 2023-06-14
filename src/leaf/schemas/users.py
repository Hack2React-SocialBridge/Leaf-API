from pydantic import BaseModel, PositiveInt


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class LoginSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    class Config:
        orm_mode = True

    id: PositiveInt
    email: str
    first_name: str
    last_name: str
    disabled: bool = True


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
