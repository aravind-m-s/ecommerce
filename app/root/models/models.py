import datetime
from uuid import uuid4
from sqlalchemy import Boolean, Column, Uuid, String, DateTime
from app.base import Base
from app.enum.user_types import UserType


class User(Base):
    __tablename__ = "users"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    type = Column(String, nullable=False, default=UserType.USER.value)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )
