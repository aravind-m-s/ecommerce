from fastapi import APIRouter, Depends
from app.apps.user.modules.auth.auth import login, register


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router.post("/login")(login)
router.post("/register")(register)
