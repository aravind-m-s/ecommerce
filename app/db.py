import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

from app.root.models import models

load_dotenv()


engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def migrate():
#     user.Base.metadata.create_all(bind=engine)
#     pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
