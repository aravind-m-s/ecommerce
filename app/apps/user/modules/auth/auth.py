import re
from fastapi import Depends
from sqlalchemy.orm import Session
from app.apps.user.schemas.user import CreateUser, Login, LoginResponse
from app.db import get_db
from app.enum.user_types import UserType
from app.exceptions import CustomException
from app.services.password_hash import hash_password, verify_password
from app.services.token import create_access_token
from app.apps.user.models.models import User
from app.services.email_validator import is_valid_email


def login(user: Login, db: Session = Depends(get_db)):

    if not is_valid_email(user.email):
        raise CustomException(status_code=422, data={"email": "Invalid email"})

    db_user = (
        db.query(User)
        .filter(User.email == user.email and User.type == UserType.USER.name)
        .first()
    )

    if not db_user:
        raise CustomException(status_code=422, data={"email": "Invalid email"})

    if not db_user.status:
        raise CustomException(status_code=422, data={"email": "User is not active"})

    if not verify_password(user.password, db_user.password):
        raise CustomException(status_code=422, data={"password": "Invalid password"})

    response_user = LoginResponse.model_validate(db_user)
    token = create_access_token({"id": str(db_user.id), "email": db_user.email})
    response_user.access_token = token
    db.close()
    return response_user


def register(user: CreateUser, db: Session = Depends(get_db)):

    if not is_valid_email(user.email):
        raise CustomException(status_code=422, data={"email": "Invalid email"})

    db_user = (
        db.query(User)
        .filter(User.email == user.email, User.type == UserType.USER.name)
        .first()
    )

    if db_user:
        raise CustomException(status_code=422, data={"email": "User already exists"})

    user.password = hash_password(user.password)

    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()

    response_user = LoginResponse.model_validate(db_user)
    token = create_access_token({"id": str(db_user.id), "email": db_user.email})
    response_user.access_token = token
    return response_user
