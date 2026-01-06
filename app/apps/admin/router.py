from fastapi import APIRouter, Depends
from app.apps.admin.modules.user.router import router as user_router
from app.services.token import validate_token


router = APIRouter(dependencies=[Depends(validate_token)])

router.include_router(user_router)
