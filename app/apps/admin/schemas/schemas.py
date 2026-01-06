from typing import Optional
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


class Category(BaseModel):
    id: UUID
    name: str


class Product(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: Category


class CreateUpdateProduct(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    parent_id: Optional[UUID] = None
    category_id: UUID


class CreateUpdateCategory(BaseModel):
    name: str
