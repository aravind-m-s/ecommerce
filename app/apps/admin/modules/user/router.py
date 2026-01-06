from fastapi import APIRouter

from app.apps.admin.modules.user.user import (
    create_user,
    delete_user,
    get_user_details,
    list_user,
    update_user,
    update_user_status,
)

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


router.post("/create")(create_user)
router.get("/list")(list_user)
router.put("/update/{user_id}")(update_user)
router.put("/status/update/{user_id}")(update_user_status)
router.delete("/delete/{user_id}")(delete_user)
router.get("/details/{user_id}")(get_user_details)

