from uuid import UUID
from pydantic import BaseModel

from app.enum.user_types import UserType


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    type: UserType


class UpdateUser(CreateUser):
    status: bool
