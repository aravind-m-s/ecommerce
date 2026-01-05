from fastapi import FastAPI
from fastapi.openapi.models import HTTPBearer
from starlette.responses import JSONResponse
from app.apps.user.router import router as user_router
from app.exceptions import CustomException


app = FastAPI(
    title="Ecommerce API",
    description="Ecommerce API",
    version="0.0.1",
    docs_url=None,
)

user_app = FastAPI(
    title="User API",
    description="User API",
    version="0.0.1",
)

user_app.include_router(user_router)


admin_app = FastAPI(
    title="Admin API",
    description="Admin API",
    version="0.0.1",
)

app.mount("/user", user_app)
app.mount("/admin", admin_app)

# migrate()


@admin_app.exception_handler(CustomException)
@user_app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    content = exc.data
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )
