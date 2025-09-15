from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Union


class LinkCreate(BaseModel):
    original_url: HttpUrl


class Link(BaseModel):
    id: int
    short_code: str
    original_url: HttpUrl
    visit_count: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[int, None] = None
