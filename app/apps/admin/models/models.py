import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Uuid,
    null,
)
from sqlalchemy.orm import relationship
from app.base import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Uuid, primary_key=True, nullable=False, index=True)
    parent_id = Column(
        Uuid,
        ForeignKey("products.id"),
        nullable=True,
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    price = Column(Float, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(Uuid, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    deleted_at = Column(
        DateTime,
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )
    status = Column(Boolean, nullable=True, default=True)

    parent = relationship("Product", remote_side=[id], back_populates="children")

    category = relationship(
        "Category", back_populates="products", foreign_keys=[category_id]
    )

    children = relationship(
        "Product", back_populates="parent", foreign_keys=[parent_id]
    )


class Category(Base):
    __tablename__ = "categories"
    id = Column(Uuid, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    status = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=True,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    products = relationship("Product", back_populates="category")
