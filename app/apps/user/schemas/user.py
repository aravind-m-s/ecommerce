from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    name: str
    email: str


class CreateUser(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class LoginResponse(Login):
    id: UUID
    access_token: str = ""

    class Config:
        from_attributes = True
