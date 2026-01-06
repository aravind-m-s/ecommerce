from sqlalchemy.orm import Session
from fastapi import Depends

from app.apps.admin.schemas.schemas import CreateUpdateProduct
from app.db import get_db
from sqlalchemy import select
from app.apps.admin.models.models import Product, Category
from app.exceptions import CustomException
from app.apps.admin.schemas.schemas import (
    Product as SchemaProduct,
    CreateUpdateCategory,
    Category as SchemaCategory,
)


def create_product(product: CreateUpdateProduct, db: Session = Depends(get_db)):
    if product.name.strip() == "":
        raise CustomException(
            status_code=422, data={"name": "Product name is required"}
        )

    if product.category_id.__str__().strip() == "":
        raise CustomException(
            status_code=422, data={"category_id": "Category is required"}
        )

    if product.price <= 0:
        raise CustomException(
            status_code=422, data={"price": "Price should be greater than 0"}
        )

    if product.stock <= 0:
        raise CustomException(
            status_code=422, data={"stock": "Stock should be greater than 0"}
        )

    db_category = db.get(Category, product.category_id)
    if not db_category:
        raise CustomException(
            status_code=422, data={"category_id": "Category not found"}
        )

    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    schema_product = SchemaProduct(
        name=db_product.name,
        price=db_product.price,
        stock=db_product.stock,
        description=db_product.description,
        category=SchemaCategory(
            id=db_category.id,
            name=db_category.name,
        ),
        id=db_product.id,
    )
    return schema_product


def list_products(db: Session = Depends(get_db)):
    stmt = select(Product).where(
        # Product.deleted_at == None,
        Product.status
        == True,
    )
    db_products = db.execute(stmt).all()
    return [
        SchemaProduct.model_validate(
            {
                **product.__dict__,
                "category": SchemaCategory.model_validate(product.category.__dict__),
            }
        )
        for product in db_products
    ]
