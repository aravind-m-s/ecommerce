from fastapi import FastAPI
from starlette.responses import JSONResponse
from app.root.router import router as root_router
from app.exceptions import CustomException
from app.apps.admin.router import router as admin_router


app = FastAPI(
    title="Ecommerce API",
    description="Ecommerce API",
    version="0.0.1",
)
app.include_router(root_router)

user_app = FastAPI(
    title="User API",
    description="User API",
    version="0.0.1",
)


admin_app = FastAPI(
    title="Admin API",
    description="Admin API",
    version="0.0.1",
)
admin_app.include_router(admin_router)

app.mount("/user", user_app)
app.mount("/admin", admin_app)

# migrate()


@app.exception_handler(CustomException)
@admin_app.exception_handler(CustomException)
@user_app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    content = exc.data
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )
