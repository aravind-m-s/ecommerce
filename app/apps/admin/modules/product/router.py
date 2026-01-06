from fastapi import APIRouter

from app.apps.admin.modules.product.product import create_product, list_products


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

router.post("/create")(create_product)
router.get("/list")(list_products)
