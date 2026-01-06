from fastapi import APIRouter, Depends
from app.apps.admin.modules.user.router import router as user_router
from app.apps.admin.modules.product.router import router as product_router
from app.services.token import validate_token


router = APIRouter(dependencies=[Depends(validate_token)])

router.include_router(user_router)
router.include_router(product_router)
