from datetime import datetime
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from app import db
from app.apps.admin.schemas.schemas import CreateUser, UpdateUser
from app.exceptions import CustomException
from app.root.models.models import User
from app.root.schemas.user import User as SchemaUser
from app.services.password_hash import hash_password


def create_user(user: CreateUser, db: Session = Depends(db.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise CustomException(status_code=422, data={"email": "User already exists"})
    user.password = hash_password(user.password)
    db_user = User(**user.model_dump())
    db_user.type = user.type.value
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return SchemaUser.model_validate(db_user.__dict__)


def list_user(db: Session = Depends(db.get_db)):
    db_users = db.query(User).filter(User.deleted_at == None).all()
    db.close()
    users = [SchemaUser.model_validate(user.__dict__) for user in db_users]
    return users


def update_user(user_id: UUID, user: UpdateUser, db: Session = Depends(db.get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise CustomException(status_code=422, data={"email": "User not found"})
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = hash_password(user.password)
    db_user.type = user.type.value
    db_user.status = user.status
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return SchemaUser.model_validate(db_user.__dict__)


def update_user_status(user_id: UUID, status: bool, db: Session = Depends(db.get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise CustomException(status_code=422, data={"email": "User not found"})
    db_user.status = status
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return SchemaUser.model_validate(db_user.__dict__)


def delete_user(user_id: UUID, db: Session = Depends(db.get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise CustomException(status_code=422, data={"email": "User not found"})
    db_user.deleted_at = datetime.now()
    db.add(db_user)
    db.commit()
    db.close()
    return "Deleted"


def get_user_details(user_id: UUID, db: Session = Depends(db.get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise CustomException(status_code=422, data={"email": "User not found"})
    db.close()
    return SchemaUser.model_validate(db_user.__dict__)
